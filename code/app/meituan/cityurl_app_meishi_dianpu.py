#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.HtmlSource import HtmlSource
from common.Rule import Rule
from common.inc_conn import Conn_mysql
from common.inc_file import File_file,File_floder
from common.inc_csv import  Csv_base
import time
import uuid
from lxml import html

htmlSource = HtmlSource()
rule = Rule()
meituan_mysql = Conn_mysql( host='localhost', user='root', passwd='514840279@qq.com', db='app', port=3306,) # 生成MYSQL数据库索引数据实例


path = 'D:/app/meituan/'
# 多页
def main():
    sql ="""
    SELECT * FROM `meituan_city_url`
        WHERE ci_name = '美食'
        AND state=1
        ORDER BY city ASC
    """
    res,data = meituan_mysql.read_sql(sql)
    files = File_file()
    for row in data:
        file_name = row['pinyin']+".json"
        json_file = files.open_source(path,file_name)
        print(json_file)


if __name__ == '__main__': # 判断文件入口
    main()
