#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.HtmlSource import HtmlSource
from common.Rule import Rule
# from common.inc_conn import Conn_mysql
from common.inc_file import File_file,File_floder
from common.inc_csv import  Csv_base
import time

htmlSource = HtmlSource()
rule = Rule()
path = 'D:/newpro/9.1'

# 多线程
def read_detial(url):
    detial_html = htmlSource.get_html(url_p=url, type_p='rg')
    #print(detial_html)
    # 写html
    files = File_file()
    names = url.split('/')
    file_name = names[len(names)-1]

    files.save_source(path=path,file=file_name, all_the_text=detial_html , encoding_='utf-8')
    colum=[
        ('title','//h1[@class="article-main-title"]//text()','l'),
        ('pushDate', '//span[@class="time"]//text()', 'arr',0),
        ('content','//div[@class="article-left"]//div[@class="article-content"]//text()','sarra',',')
   ]
    result = rule.html_content_analysis_detial(html_text=detial_html, column=colum, url=url)
    print(result)
    #sql="insert into cancer value('%s','%s','%s','%s','%s')"%(result[0][1][0],str(result[1][1][0]).replace('患者,图片因隐私问题无法显示','').replace("患者,","患者:").replace("医生,","医生:").replace('\'','"'),type,'春雨医生',url)
    #print(sql)
    # 写文件
    # web_name（网站名）、web_url（网址）、titile（标题）、text（新闻内容）、publish_date（发布时间）
    csv = Csv_base()
    csv.write_csv_file_line(file_path=path + "/data.csv", str=['中华军事网', url, result[0][1], result[1][1], result[2][1],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))])



# 多页
def main():
    floder = File_floder()
    floder.add(path_p=path)
    csv = Csv_base()
    csv.write_csv_file_line(file_path=path+"/data.csv",mode='w+',str=['网站名','网址','标题','新闻内容','发布时间','采集时间'])
    # 爬虫
    start_url = "https://military.china.com/news/"

    #print(url)
    list_html = htmlSource.get_html(url_p=start_url,type_p='rg')
    #print(list_html)
    colum=[('a','//div[@class="column-list"]//h3[@class="tit"]//a//@href','l')]
    list = rule.html_content_analysis_detial(html_text=list_html,column=colum,url=start_url)
    #print(list)
    for a in list[0][1]:
        read_detial(a)
       # th = threading.Thread(target=read_detial, args=(a))
       # th.start()  # 启动线程


if __name__ == '__main__': # 判断文件入口
    main()
