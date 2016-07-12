#!/usr/bin/env python
# -*- coding: utf-8 -*-'

import db_con as db_con
from xml.dom.minidom import parse, parseString
from time_utility import *
import subprocess
import os
from util.color import in_red
from util.readstate import read_run_model


def singleton(cls, *argus, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*argus, **kw)
        return instances[cls]

    return _singleton


# @singleton
class DBHolder(object):
    def __init__(self):
        run_model = read_run_model()
        if run_model == 1:
            self.configfile = "config/dbconfig1.xml"
        if run_model == 2:
            self.configfile = "config/dbconfig2.xml"
        self.DBMAP = {}
        self.parseconfig()
        self.conpool = {}

    def __del__(self):
        for dbid in self.conpool:
            for tp in self.conpool[dbid]:
                if self.conpool[dbid][tp].open:
                    self.conpool[dbid][tp].close()

    def parseconfig(self):
        rootnode = parse(self.configfile)

        servers = rootnode.getElementsByTagName("servers")[0]
        for server in servers.getElementsByTagName("server"):
            stype = server.getAttribute("type")
            username = server.getElementsByTagName("username")[0]
            password = server.getElementsByTagName("password")[0]
            publicip = server.getElementsByTagName("ip")[0]
            intraip = server.getElementsByTagName("intraip")[0]
            port = server.getElementsByTagName("port")[0]
            nodes = (username, password, publicip, intraip, port)

            for db in server.getElementsByTagName("db"):
                dbid = db.getAttribute("id")
                dbname = db.getAttribute("dbname")
                self.DBMAP.setdefault(dbid, {}).setdefault(stype, dict(
                        (node.nodeName, node.firstChild.nodeValue) for node in nodes))
                self.DBMAP[dbid][stype]["dbname"] = dbname

    def getconn(self, dbid, tp="main"):
        if not self.DBMAP.get(dbid, None):
            exit("wrong database: %s" % dbid)
        if self.conpool.get(dbid, {}).get(tp, None) and self.conpool[dbid][tp].reconnect:
            return self.conpool[dbid][tp]
        dbinfo = self.DBMAP[dbid].get(tp, None)
        for t in ["backup", "mid", "main", '']:
            if dbinfo:
                print dbinfo
                conn = db_con.Conn(dbinfo['intraip'], int(dbinfo['port']), dbinfo["dbname"], dbinfo['username'],
                                   dbinfo['password'])
                if conn.open:
                    print "Connection %s@%s USED!" % (dbinfo['intraip'], dbinfo["dbname"])
                    self.conpool.setdefault(dbid, {}).setdefault(tp, conn)
                    return conn
            print "%s %s can't be used, try default %s" % (tp, dbid, t)
            dbinfo = self.DBMAP[dbid].get(t, None)

    def getdbname(self, dbid, tp="main"):
        return self.DBMAP[dbid][tp]["dbname"]

    def getgameserverconn(self, host, port, dbname):
        dbinfo = self.DBMAP["Login"]["backup"]
        return db_con.Conn(host, port, dbname, dbinfo['username'], dbinfo['password'])

    def getrecordconn(self, date):
        weekid = weekofyear(date)
        if self.conpool.get("record", {}).has_key(weekid):
            return self.conpool["record"][weekid]
        ossconn = self.getconn("OSS", "backup")
        sql = "select slave_ip, slave_port, slave_dbname from t_ossdb_list where week_id = %s " % weekid
        result = ossconn.queryone(sql)
        dbinfo = self.DBMAP["OSS"]["main"]
        recordconn = db_con.Conn(result[0], result[1], result[2], dbinfo['username'], dbinfo['password'])
        self.conpool.setdefault("record", {}).setdefault(weekid, recordconn)
        return recordconn

    def getrecordmainconn(self, date):
        weekid = weekofyear(date)
        if self.conpool.get("record", {}).has_key(weekid):
            return self.conpool["record"][weekid]
        ossconn = self.getconn("OSS", "backup")
        sql = "select host_ip, port, dbname from t_ossdb_list where week_id = %s " % weekid
        result = ossconn.queryone(sql)
        print result[0], result[1]
        dbinfo = self.DBMAP["OSS"]["main"]
        recordconn = db_con.Conn(result[0], result[1], result[2], dbinfo['username'], dbinfo['password'])
        self.conpool.setdefault("record", {}).setdefault(weekid, recordconn)
        return recordconn

    def mysql_exc(self, dbid, sql, tp='main'):
        dbinfo = self.DBMAP[dbid].get(tp, None)
        exc_str = """mysql -u%s -p%s -h%s -P%s -e\"%s\"""" % (dbinfo['username'], dbinfo['password'],
                                                              dbinfo['intraip'], int(dbinfo['port']), sql)
        p = subprocess.Popen(exc_str, shell=True)
        return_code = p.wait()
        if return_code == 1:
            print in_red(sql)
            return False
        else:
            return True

    def export(self, dbinfo, sql, additional_str):
        exc_str = """mysql -u%s -p%s -h%s -P%s -Ne\"%s\"""" % (dbinfo['username'], dbinfo['password'],
                                                               dbinfo['dbip'], int(dbinfo['dbport']), sql) + \
                  additional_str
        p = subprocess.Popen(exc_str, shell=True)
        return_code = p.wait()
        if return_code == 1:
            print in_red(sql)
            return False
        else:
            return True

dbholder = DBHolder()
