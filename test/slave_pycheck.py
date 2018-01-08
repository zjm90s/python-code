# -*- coding: utf-8 -*-
__author__ = 'jianming.zhou'

import pytorndb


print "\033[1;32m-----------------------------------------------------------------------------\033[0m"
db_name = "my_db"
m_db = pytorndb.Connection("localhost:3306", db_name, user="zjm", password="654321")
s_db = pytorndb.Connection("localhost:3306", db_name, user="zjm", password="654321")
m_tbcount = m_db.get("select count(*) as count from information_schema.tables where table_schema = '%s'" % (db_name)).get("count")
s_tbcount = s_db.get("select count(*) as count from information_schema.tables where table_schema = '%s'" % (db_name)).get("count")
tables = m_db.query("select table_name from information_schema.tables where table_schema = '%s'" % (db_name))
total_data_count = 0
tblist = []

for tb in tables:
    table = tb.get("table_name")
    try:
        m_count = m_db.get("select count(*) as count from %s" % (table)).get("count")
        s_count = s_db.get("select count(*) as count from %s" % (table)).get("count")
        total_data_count += m_count
        tblist.append((table, m_count, s_count))
    except BaseException:
        count = s_db.get("select count(*) as count from information_schema.tables where table_schema = '%s'" % (db_name)).get("count")
        if count == 0:
            print "\033[1;31m [%s] Slave中不存在 \033[0m" % (table)
        else:
            print "\033[1;31m [%s] 查询异常 \033[0m" % (table)

tblist.sort(key=lambda tb: tb[1], reverse=True)
for tb in tblist:
    table = tb[0]
    m_count = tb[1]
    s_count = tb[2]
    if m_count == s_count:
        print " [%s] master_count:%d slave_count:%d " % (table, m_count, s_count)
    else:
        print "\033[1;31m [%s] master_count:%d slave_count:%d \033[0m" % (table, m_count, s_count)
print "\033[1;32m master_table_count:%d, slave_table_count:%d, total_data_count:%s \033[0m" % (m_tbcount, s_tbcount, total_data_count)

m_db.close()
s_db.close()
print "\033[1;32m-----------------------------------------------------------------------------\033[0m"