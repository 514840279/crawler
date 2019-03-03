#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.HtmlSource import HtmlSource
from common.Rule import Rule
from common.inc_conn import Conn_mysql
from common.inc_file import File_file,File_floder
from common.inc_csv import  Csv_base
import time
import uuid

htmlSource = HtmlSource()
rule = Rule()
meituan_mysql = Conn_mysql( host='localhost', user='root', passwd='514840279@qq.com', db='app', port=3306) # 生成MYSQL数据库索引数据实例



# 多页
def main():
    # 爬虫
    start_url = "https://www.meituan.com/changecity/"
    #print(url)
    list_html = htmlSource.get_html(url_p=start_url,type_p='rg')
    #print(list_html)
    colum=[('name','//div[@class="alphabet-city-area"]//div[@class="city-area"]//span[@class="cities"]//a//text()','l'),
           ('a','//div[@class="alphabet-city-area"]//div[@class="city-area"]//span[@class="cities"]//a//@href','sab','https:')]
    list = rule.html_content_analysis_detial(html_text=list_html,column=colum,url=start_url)
    maxSize = len(list[0][1])-1
    for a in  range(0, maxSize) :
        sql = "insert into meituan_city_url value('%s','%s','%s','%d','%d',null,'%s')" % (uuid.uuid4(),list[0][1][a],list[1][1][a],1,1,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        print(sql)
        meituan_mysql.write_sql(sql)


if __name__ == '__main__': # 判断文件入口
    main()
