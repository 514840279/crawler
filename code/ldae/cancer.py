#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.HtmlSource import HtmlSource
from common.Rule import Rule
from common.inc_conn import Conn_mysql

htmlSource = HtmlSource()
rule = Rule()
ldae_mysql = Conn_mysql( host='localhost', user='root', passwd='root', db='ldae', port=3306) # 生成MYSQL数据库索引数据实例

# 多线程
def read_detial(url,type):
    detial_html = htmlSource.get_html(url_p=url, type_p='rg')
    #print(detial_html)
    colum=[
        ('title','//div[@class="ui-grid ui-main clearfix"]//div[@class="bread-crumb-spacial"]//span[@class="title"]//text()','l'),
        ('content','//div[@class="main-wrap"]//div[@class="problem-detail-wrap"]//div[@class="block-line"]//div[@class="context-left"]//text()','sarra',',')
   ]
    result = rule.html_content_analysis_detial(html_text=detial_html, column=colum, url=url)
    #print(result)
    sql="insert into cancer value('%s','%s','%s','%s','%s')"%(result[0][1][0],str(result[1][1][0]).replace('患者,图片因隐私问题无法显示','').replace("患者,","患者:").replace("医生,","医生:").replace('\'','"'),type,'春雨医生',url)
    print(sql)
    ldae_mysql.write_sql(sql=sql)

# 多页
def main():
    start_url = "https://www.chunyuyisheng.com/pc/search/qalist/?query=%s&page=%d"
    str = ["肺癌"," 肝癌","乳腺癌","胃癌","直肠癌"] 
    for ss in str:
        for i in range(1,51):
            url = start_url%(ss,i)
            #print(url)
            list_html = htmlSource.get_html(url_p=url,type_p='rg')
            #print(list_html)
            colum=[('a','//div[@class="hot-qa main-block"]//div//div[@class="qa-item qa-item-ask"]//a//@href','sab','https://www.chunyuyisheng.com')]
            list = rule.html_content_analysis_detial(html_text=list_html,column=colum,url=url)
            print(list)
            for a in list[0][1]:
                read_detial(a, ss)
                #th = threading.Thread(target=read_detial, args=(a,str))
                #th.start()  # 启动线程


if __name__ == '__main__': # 判断文件入口
    main()
