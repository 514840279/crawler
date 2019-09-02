#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from common.Mysql_Utils import MyPymysqlPool
import json, hashlib,pymysql




def run():
    dbconn = MyPymysqlPool("default")
    myMd5 = hashlib.md5()

    sql = "select  * from 电影天堂_detail t where 下载地址 !='' and not exists(select 1 from addr_thund a  where t.`主键` = a.`主键`)"
    result = dbconn.getAll(sql)

    for row in result:
        addrjson = row["下载地址"]
        jsonarr = json.loads(str(addrjson).replace("\'", "\""), encoding="utf-8")
        for addrobj in jsonarr:
            addr = addrobj["地址"]
            if addr != "":
                if isinstance(addr,list):
                    for add in addr:
                        insertdata(dbconn, row["主键"],  add)
                insertdata(dbconn, row["主键"],  addr)
    dbconn.dispose()

def insertdata(dbconn,mainid,addr):

    myMd5 = hashlib.md5()
    try:
        myMd5.update(addr.encode("utf8"))
        uuid = myMd5.hexdigest()
    except Exception as e:
        print(e, addr)
    insersql = " insert into addr_thund(uuid,主键,addr) values('%s','%s','%s')" % (
        uuid, mainid, addr)
    try:
        dbconn.insert(insersql)
    except pymysql.err.IntegrityError as pei:
        pass
    except pymysql.err.ProgrammingError as pep:
        print(pep, insersql)
    except Exception as e:
        create = "create table addr_thund(uuid varchar(36) primary key,主键 varchar(36),addr varchar(2000)," \
                 "更新时间 timestamp on update current_timestamp) "
        dbconn.update(create)
        dbconn.insert(insersql)
    dbconn.end("commit")

if __name__ == '__main__':
    run()
