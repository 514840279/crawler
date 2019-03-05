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
import re
htmlSource = HtmlSource()
rule = Rule()
meituan_mysql = Conn_mysql( host='localhost', user='root', passwd='514840279@qq.com', db='app', port=3306,) # 生成MYSQL数据库索引数据实例


path = 'D:/app/meituan/'
# 多页
def main():
    floder = File_floder()
    floder.add(path_p=path)

    sql ="""
    SELECT * FROM `meituan_city_url`
        WHERE ci_name = '美食'
        AND state<100
        ORDER BY city ASC
    """
    res,data = meituan_mysql.read_sql(sql)
    files = File_file()
    for row in data:
        url = row['ci']
        json_file_name=row['pinyin']+".json"
        print(path+json_file_name)
        #print(row)
        html_source = htmlSource.get_html(url_p=url,type_p='rg')
        #print(html_source)
        regex_text = re.search(r'_appState = (.*?);',html_source).group(1)
        #print(regex_text)
        files.save_source(path,json_file_name,regex_text)



if __name__ == '__main__': # 判断文件入口
    main()
