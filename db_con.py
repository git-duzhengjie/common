# coding: utf-8
#
# 该模块用于处理与数据库相关主题的功能
# 包括数据库的连接、查询、sql执行、sql批量执行、数据导入、数据库重连、数据库关闭、定制特定的返回类型
# 比如：列表、字典、整型、字符串等
#

from __future__ import division
import MySQLdb
import datetime
from util.record import write_tsv, write_csv
import traceback


class Conn:
    def __init__(self, host, port, database, user, password):
        """
        连接数据库
        :param host: 数据库IP
        :param port: 数据库端口
        :param database: 数据库名
        :param user: 用户名
        :param password: 密码
        """
        self.ip = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        try:
            self.conn = MySQLdb.connect(host=self.ip, user=self.user, passwd=self.password, db=self.database,
                                        port=self.port)
            self.cur = self.conn.cursor()
        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    @property
    def reconnect(self):
        """
        数据库重连
        :return: 连接成功返回True，连接失败返回False
        """
        if not self.open:
            try:
                self.conn = MySQLdb.connect(host=self.ip, user=self.user, passwd=self.password, db=self.database,
                                            port=self.port)
                self.cur = self.conn.cursor()
                return True
            except MySQLdb.Error as e:
                print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
                return False
        try:
            self.conn.ping()
            return True
        except MySQLdb.Error as e:
            try:
                self.conn = MySQLdb.connect(host=self.ip, user=self.user, passwd=self.password, db=self.database,
                                            port=self.port)
                self.cur = self.conn.cursor()
                return True
            except MySQLdb.Error as e:
                print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
                return False

    @property
    def open(self):
        """
        判断连接是否可用
        :return: 可用返回True，不可用返回False，异常返回None
        """
        try:
            return self.conn.open
        except MySQLdb.Error:
            print("Connection %s:%s@%s failed" % (self.ip, self.port, self.database))
            return None

    def querynum(self, sql):
        count = self.cur.execute(sql)
        result = self.cur.fetchone()
        reval = result[0]
        if reval is None:
            return 0
        return reval

    def excute(self, sql, ps=None):
        if not ps:
            return self.cur.execute(sql)
        else:
            return self.cur.execute(sql, ps)

    def fetchall(self):
        return self.cur.fetchall()

    def fetchone(self):
        return self.cur.fetchone()

    def query(self, sql):
        count = self.cur.execute(sql)
        reval = []
        if count == 0:
            return reval
        for i in range(count):
            result = self.cur.fetchone()
            reval.append(result[0])
        return reval

    def queryone(self, sql):
        count = self.cur.execute(sql)
        if count == 0:
            return ""
        result = self.cur.fetchone()
        return result

    def queryall(self, sql):
        count = self.cur.execute(sql)
        if count == 0:
            return ""
        result = self.cur.fetchall()
        return result

    def queryset(self, sql):
        ret_set = {}
        count = self.cur.execute(sql)
        for i in range(count):
            rs = self.cur.fetchone()
            ret_set[rs[0]] = 1
        return ret_set

    def querystring(self, sql):
        count = self.cur.execute(sql)
        if count == 0:
            return "\'0\'"
        reval = []
        for i in range(count):
            result = self.cur.fetchone()
            tmp = "\'%s\'" % (result[0])
            reval.append(tmp)
        return ','.join(reval)

    def querynums(self, sql):
        count = self.cur.execute(sql)
        if count == 0:
            return "0"
        reval = []
        for i in range(count):
            result = self.cur.fetchone()
            tmp = "%s" % (result[0])
            reval.append(tmp)
        return ','.join(reval)

    def querynumrows(self, sql):
        return self.cur.execute(sql)

    def querylist(self, sql):
        count = self.cur.execute(sql)
        if not count:
            return []
        reval = []
        for i in range(count):
            result = self.cur.fetchone()
            reval.append(result)
        return reval

    def querymap(self, sql):
        count = self.cur.execute(sql)
        if not count:
            return {}
        reval = {}
        for i in range(count):
            result = self.cur.fetchone()
            if isinstance(result[1], datetime.date):
                tmpk = result[1].strftime("%Y-%m-%d")
            else:
                tmpk = result[1]
            reval.setdefault(tmpk, result[0])
        return reval

    def querytuplemap(self, sql, num):
        count = self.cur.execute(sql)
        if not count:
            return {}
        reval = {}
        for i in range(count):
            result = self.cur.fetchone()
            tmpk = []
            for j in range(num):
                tmpk.append(result[1 + j])
            tmpk = tuple(tmpk)
            reval.setdefault(tmpk, result[0])
        return reval

    def querytuplemaptuple(self, sql, numkey, numvalue):
        count = self.cur.execute(sql)
        if not count:
            return {}
        reval = {}
        for i in range(count):
            result = self.cur.fetchone()
            tmpk = []
            for j in range(numkey):
                tmpk.append(result[numvalue + j])
            tmpk = tuple(tmpk)
            tmpv = []
            for j in range(numvalue):
                tmpv.append(result[0 + j])
            reval.setdefault(tmpk, tmpv)
        return reval

    def querymaplist(self, sql):
        count = self.cur.execute(sql)
        if not count:
            return {}
        reval = {}
        for i in range(count):
            result = self.cur.fetchone()
            if isinstance(result[1], datetime.date):
                tmpk = result[1].strftime("%Y-%m-%d")
            else:
                tmpk = result[1]
            reval.setdefault(tmpk, []).append(result[0])
        return reval

    def querytuplemaplist(self, sql, num):
        count = self.cur.execute(sql)
        if not count:
            return {}
        reval = {}
        for i in range(count):
            result = self.cur.fetchone()
            tmpk = []
            for j in range(num):
                tmpk.append(result[1 + j])
            tmpk = tuple(tmpk)
            reval.setdefault(tmpk, []).append(result[0])
        return reval

    def querylistmap(self, sql):
        count = self.cur.execute(sql)
        if not count:
            return {}
        reval = {}
        for i in range(count):
            result = self.cur.fetchone()
            if isinstance(result[-1], datetime.date):
                tmpk = result[-1].strftime("%Y-%m-%d")
            else:
                tmpk = result[-1]
            reval.setdefault(tmpk, result[:-1])
        return reval

    def querylistmaplist(self, sql):
        count = self.cur.execute(sql)
        if not count:
            return {}
        reval = {}
        for i in range(count):
            result = self.cur.fetchone()
            if isinstance(result[-1], datetime.date):
                tmpk = result[-1].strftime("%Y-%m-%d")
            else:
                tmpk = result[-1]
            reval.setdefault(tmpk, []).append(result[:-1])
        return reval

    def showcreatetable(self, tb):
        ret = ''
        count = self.cur.execute('show create table %s' % tb)
        if count == 0:
            return ret
        rs = self.cur.fetchone()
        return rs[1]

    def clonetable(self, src, tb):
        try:
            tb_desc = src.showcreatetable(tb)
            if tb_desc == '':
                return -1
            self.excute(tb_desc)
            self.commit()
            return 0
        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    @staticmethod
    def formatinsert(table, fds_num, ignore=False):
        if not ignore:
            string = 'insert into ' + table + ' values('
        else:
            string = 'insert ignore into ' + table + ' values('
        for i in range(0, fds_num - 1):
            string += '%s,'
        string += '%s)'
        return string

    def deleteall(self, tb):
        self.cur.execute("delete from %s" % tb)
        self.conn.commit()

    def batch_excute(self, ary, batch_num, insert_str):
        try:
            ary_len = len(ary)
            tmp_ary = []
            for i in range(0, ary_len):
                tmp_ary.append(ary[i])
                if (i + 1) % batch_num == 0:
                    self.cur.executemany(insert_str, tmp_ary)
                    tmp_ary = []
                elif i == ary_len - 1:
                    self.cur.executemany(insert_str, tmp_ary)
                    tmp_ary = []
                self.conn.commit()
            return True
        except MySQLdb.Error as e:
            print("Mysql Error %s: %s" % (e.args[0], e.args[1]))
            return False
        except MySQLdb.Warning, w:
            print("MySQL Warning:%s" % str(w))

    def close(self):
        self.cur.close()
        self.conn.close()

    def commit(self):
        return self.conn.commit()

    def load_data(self, data, table):
        try:
            write_tsv(data)
            sql = "load data local infile 'tmp' REPLACE INTO table %s fields terminated by '\t'"
            self.excute(sql % table)
            return True
        except:
            traceback.print_exc()
            return False

    def insert_data(self, data, table):
        try:
            if len(data) < 10000:
                if self.batch_excute(data, 1000, self.formatinsert(table, len(data[0]))):
                    return True
            else:
                if self.load_data(data, '%s' % table):
                    return True
            return False
        except:
            traceback.print_exc()
            print(table, data[0], self.formatinsert(table, len(data[0])))
            return False

    def table_exist(self, table):
        tables = self.query("show tables")
        if table in tables:
            return True
        else:
            return False

    def create_table(self, table, item, variables):
        try:
            item_str = ''
            for i in item:
                item_str += i + ' ' + variables.get(i, 'varchar(256)') + ','
            item_str = item_str.rstrip(',')
            print("create table %s (%s)" % (table, item_str))
            self.excute("create table %s (%s)" % (table, item_str))
            return True
        except MySQLdb.Error as e:
            print("Mysql Error %s: %s" % (e.args[0], e.args[1]))
            return False

