#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.HtmlSource import HtmlSource
from common.Rule import Rule
from common.inc_conn import Conn_mysql
from common.inc_file import File_file,File_floder
from common.inc_csv import  Csv_base
import time

htmlSource = HtmlSource()
rule = Rule()
meituan_mysql = Conn_mysql( host='localhost', user='root', passwd='root', db='app', port=3306) # 生成MYSQL数据库索引数据实例

# 多线程
def read_detial(url,i):
    detial_html = htmlSource.get_html(url_p=url, type_p='rg')
    #print(detial_html)
    colum=[
        ('title','//h1[@class="main-title"]//text()','l'),
        ('pushDate', '//span[@class="date"]//text()', 'l'),
        ('content','//div[@class="article"]//text()','sarra',',')
   ]
    result = rule.html_content_analysis_detial(html_text=detial_html, column=colum, url=url)
    print(result)
    sql="insert into cancer value('%s','%s','%s','%s','%s')"%(result[0][1][0],str(result[1][1][0]).replace('患者,图片因隐私问题无法显示','').replace("患者,","患者:").replace("医生,","医生:").replace('\'','"'),type,'春雨医生',url)
    #print(sql)
    meituan_mysql.write_sql(sql)


# 多页
def main():
    sql ="""
    SELECT * FROM `meituan_city_url`
        WHERE url LIKE 'https://i.meituan.com/%'
        AND state<100
        ORDER BY url ASC,current_page DESC
    """
    res,data = meituan_mysql.read_sql(sql)

    for i in range(1,len(data)-1):
        url = data['url']
        #print(url)
        list_html = htmlSource.get_html(url_p=url,type_p='rg')
        #print(list_html)
        colum=[('a','//div[@class="fixList"]//ul//li//a//@href','l')]
        list = rule.html_content_analysis_detial(html_text=list_html,column=colum,url=url)
        #print(list)
        for a in list[0][1]:
            if(a[len(a)-6:]=='.shtml'):
                read_detial(a,i)
           # th = threading.Thread(target=read_detial, args=(a))
           # th.start()  # 启动线程


if __name__ == '__main__': # 判断文件入口
    main()
