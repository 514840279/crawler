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



# 多页
def main():
    sql ="""
    SELECT * FROM `meituan_city_url`
        WHERE url LIKE 'https://i.meituan.com/%'
        AND state<100
        and ci is null
        ORDER BY url ASC
    """
    res,data = meituan_mysql.read_sql(sql)
    colum = [('a', '//ul[@class="icon-list page current"]/li[1]/a/@href', 'sab','https:'),
             ('name', '//ul[@class="icon-list page current"]/li[1]/a/span[@class="icon-desc"]/text()', 'l')]

    for row in data:
        url = row['url']
        #print(row)
        html_source = htmlSource.get_html(url_p=url,type_p='rg')
        #print(html_source)
        datat = rule.html_content_analysis_detial(html_text=html_source, column=colum, url=url)
        print(datat)
        if(len(datat[0][1])!=0):

            upda_sql = "update meituan_city_url set ci='%s',ci_name='%s' where uuid='%s'" %(datat[0][1][0],datat[1][1][0],row['uuid'])
            print(upda_sql)
            meituan_mysql.write_sql(upda_sql)

if __name__ == '__main__': # 判断文件入口
    main()
