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
meituan_mysql = Conn_mysql( host='localhost', user='root', passwd='514840279@qq.com', db='app', port=3306) # 生成MYSQL数据库索引数据实例



# 多页
def main():
    # 爬虫
    start_url = "https://i.meituan.com/index/changecity?cevent=imt%2Fhd%2FcityBottom"
    #print(url)
    list_html = htmlSource.get_html(url_p=start_url,type_p='rg')
    colum = [('name', '//div[@class="box nopadding"]/div[@class="abc"]/ul[@class="table"]/li','l')]
    list = rule.html_content_analysis_detial(html_text=list_html, column=colum, url=start_url)
    maxSize = len(list[0][1]) - 1
    datacolum = [('name', './a[@class="react"]/text()', 'l'),
                 ('a', './a[@class="react"]/@href', 'sab', 'https:'),
                 ('citypinyin', './a[@class="react"]/@data-citypinyin', 'l')]
    data = rule.html_content_analysis_list(html_text=list_html,group=colum,column=datacolum,url=start_url)

    for a in range(len(data)-1):
        row = data[a]

        if(row[0][1][0]!="更多»"):
            sql = "insert into meituan_city_url value('%s','%s','%s','%d',null,'%s','%s')" % (uuid.uuid4(),row[0][1][0],row[1][1][0],1,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),row[2][1][0])
            print(sql)
            meituan_mysql.write_sql(sql)


if __name__ == '__main__': # 判断文件入口
    main()
