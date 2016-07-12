# --*--coding:utf-8--*--
import xlrd
from util.color import *
from util.dbholder import DBHolder
import sys


def run(xl_file):
    data = open_excl(xl_file)
    sheets = data.sheets()
    sheet_names = data.sheet_names()
    db = sys.argv[1]
    tb = None
    dbholder = DBHolder()
    if len(sys.argv) == 3:
        tb = sys.argv[2]
    conn = dbholder.getconn('raw')
    create_sql_base = "create table `%s`.`%s`("
    #  创建数据库
    if tb is None:
        for database in sheet_names:
            if database != db and db != 'all':
                continue
            conn.excute("drop database %s" % database)
            conn.excute("create database %s" % database)
    # 创建表
    for i in range(len(sheets)):
        nrows = sheets[i].nrows
        ncols = sheets[i].ncols
        sheet = sheets[i]
        database = sheet_names[i]
        if database != db and db != 'all':
            continue
        table = None
        column_pk = ''
        column_index = ''
        for k in range((ncols + 1) / 3):
            for j in range(nrows):
                column = sheet.cell_value(j, 0 + k * 3)
                column_type = sheet.cell_value(j, 1 + k * 3)
                if 2 + k * 3 < ncols:
                    other = sheet.cell_value(j, 2 + k * 3)
                    if other == 'pk':
                        if column_pk == '':
                            column_pk = column
                        else:
                            column_pk = column_pk + ',' + column
                    if other == 'index':
                        if column_index == '':
                            column_index = column
                        else:
                            column_index = column_index + ',' + column
                if column_type == '' and column != '':
                    table = column
                    create_sql = create_sql_base % (database, table)
                    if tb is None:
                        conn.excute("drop table if exists `%s`.`%s`" % (database, table))
                    elif table == tb:
                        conn.excute("drop table if exists `%s`.`%s`" % (database, table))
                elif column != '' and column_type != '':
                    create_sql += "`%s` %s," % (column, column_type)
                elif column == '' and column_type == '' and table is not None:
                    create_sql = create_sql.rstrip(',')
                    if column_pk != '':
                        create_sql += ',primary key(%s)' % column_pk
                    if column_index != '':
                        create_sql += ', INDEX index0(%s)' % column_index
                    create_sql += ")"
                    if tb is None:
                        print create_sql, column_pk
                        conn.excute(create_sql)
                    elif table == tb:
                        print create_sql, column_pk
                        conn.excute(create_sql)
                    table = None
                    column_pk = ''
                    column_index = ''
                if j == nrows - 1 and table is not None:
                    create_sql = create_sql.rstrip(',')
                    if column_pk != '':
                        create_sql += ',primary key(%s)' % column_pk
                    if column_index != '':
                        create_sql += ', INDEX index0(%s)' % column_index
                    create_sql += ")"
                    if tb is None:
                        print create_sql,column_pk
                        conn.excute(create_sql)
                    elif table == tb:
                        print create_sql,column_pk
                        conn.excute(create_sql)
                    table = None
                    column_pk = ''
                    column_index = ''
    print 'init over!'
    conn.close()


def open_excl(xl_file):
    try:
        data = xlrd.open_workbook(xl_file)
        return data
    except IOError, e:
        print str(e)


run('config/datamodel.xls')
