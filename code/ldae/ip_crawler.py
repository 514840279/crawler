#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.HtmlSource import HtmlSource
from common.Rule import Rule
from common.inc_conn import Conn_mysql
import time

htmlSource = HtmlSource()
rule = Rule()
ldae_mysql = Conn_mysql( host='localhost', user='root', passwd='root', db='ldae', port=3306) # 生成MYSQL数据库索引数据实例



# 多页
def main():
    start_url = [   #("https://www.kuaidaili.com/free/inha/1018/","kuaidaili"),
                    #("https://www.kuaidaili.com/free/intr/1018/","kuaidaili"),
                    #("http://www.66ip.cn/648.html","66ip"),
                    ("http://www.goubanjia.com/free/index1.shtml","goubanjia"),
                    ("http://www.ip181.com/","ip181"),
                    ("http://www.ip3366.net/","ip3366"),
                    ("http://www.ip3366.net/free/?stype=1","ip3366"),
                    ("http://www.ip3366.net/free/?stype=2","ip3366"),
                    ("http://www.ip3366.net/free/?stype=3","ip3366"),
                    ("http://www.ip3366.net/free/?stype=4","ip3366"),
                    ("http://www.xicidaili.com/nn/","xicidaili"),
                    ("http://www.xicidaili.com/nt/","xicidaili"),
                    ("http://www.xicidaili.com/wn/","xicidaili"),
                    ("http://www.xicidaili.com/wt/","xicidaili"),
                    ("http://www.nianshao.me/?stype=1","nianshao"),
                    ("http://www.nianshao.me/?stype=2","nianshao"),
                    ("http://www.nianshao.me/?stype=5","nianshao"),
                    ("http://www.pcdaili.com/index.php?m=daili&a=free&type=1","pcdaili"),
                    ("http://www.pcdaili.com/index.php?m=daili&a=free&type=2","pcdaili"),
                    ("http://www.pcdaili.com/index.php?m=daili&a=free&type=3","pcdaili"),
                    ("http://www.pcdaili.com/index.php?m=daili&a=free&type=4","pcdaili"),
                    ("http://www.yun-daili.com/free.asp?stype=1","daili"),
                    ("http://www.yun-daili.com/free.asp?stype=2","daili"),
                    ("http://www.yun-daili.com/free.asp?stype=3","daili"),
                    ("http://www.yun-daili.com/free.asp?stype=4","daili"),
    ]

    for url in start_url:
        list_detail(url,648)


def list_detail(url,page):
    if(url==()):
        return
    print(url)
    time.sleep(5)
    list_html = htmlSource.get_html(url_p=url[0], type_p='rg')
    #print(list_html)
    colum = []
    next_url =()
    if url[1] == 'kuaidaili':
        colum = [
            ('IP', '//div[@id="list"]//table//tbody//tr//td[1]//text()', 'l'),
            ('PORT', '//div[@id="list"]//table//tbody//tr//td[2]//text()', 'l'),
            ('匿名度', '//div[@id="list"]//table//tbody//tr//td[3]//text()', 'l'),
            ('类型', '//div[@id="list"]//table//tbody//tr//td[4]//text()', 'l'),
            ('位置', '//div[@id="list"]//table//tbody//tr//td[5]//text()', 'l'),
            ('响应速度', '//div[@id="list"]//table//tbody//tr//td[6]//text()', 'l'),
            ('最后验证时间', '//div[@id="list"]//table//tbody//tr//td[7]//text()', 'l'),
        ]
        url_str =""
        if page < 2045:
            page = page +1
            url_str = url[0].replace('%d/'%(page-1),'')+"%d/"% (page)
        next_url =(url_str,url[1])
        list = rule.html_content_analysis_list(html_text=list_html, column=colum, url=url[0])
        print(list)
        for row in list:
            print(row)
            sql = "insert into ip (IP,端口,匿名度,类型,位置,响应速度,最后验证时间) value('%s','%s','%s','%s','%s','%s','%s')" % (
            row[0][1], row[1][1], row[2][1], row[3][1], row[4][1], row[5][1], row[6][1])
            print(sql)
            ldae_mysql.write_sql(sql=sql)
            # th = threading.Thread(target=read_detial, args=(a,str))
            # th.start()  # 启动线程
        list_detail(next_url, page)
    elif url[1] == '66ip':
        colum = [
            ('IP', '//div[@class="container"]//table//tr//td[1]//text()', 'l'),
            ('PORT', '//div[@class="container"]//table//tr//td[2]//text()', 'l'),
            ('匿名度', '//div[@class="container"]//table//tr//td[4]//text()', 'l'),
            ('位置', '//div[@class="container"]//table//tr//td[3]//text()', 'l'),
            ('最后验证时间', '//div[@class="container"]//table//tr//td[5]//text()', 'l'),
        ]

        #next_url = (url_str, url[1])

        list = rule.html_content_analysis_list(html_text=list_html, column=colum, url=url[0])
        print(list)
        for row in list:
            print(row)
            sql = "insert into ip (IP,端口,匿名度,位置,最后验证时间) value('%s','%s','%s','%s','%s')" % (
            row[0][1], row[1][1], row[2][1], row[3][1], row[4][1])
            print(sql)
            ldae_mysql.write_sql(sql=sql)
            # th = threading.Thread(target=read_detial, args=(a,str))
            # th.start()  # 启动线程
        next_url = (url[0].replace('%d.html'% (page),'%d.html'% (page+1)),url[1])
        page = page+1
        if page<1129:
            list_detail(next_url, page)
    elif url[1] == 'goubanjia':
        col = [("a",'//div[@id="list"]//table//tbody//tr',"l")]
        row_html = rule.html_content_analysis_list(html_text=list_html, column=col, url=url[0])
        colum = [
            ('IP', '//td[1]', 'l',':',0),
            ('PORT', '//div[@id="list"]//table//tbody//tr//td[1]//span[@class="port"]//text()', 'l',':',1),
            ('匿名度', '//div[@id="list"]//table//tbody//tr//td[2]//text()', 'l'),
            ('类型', '//div[@id="list"]//table//tbody//tr//td[3]//text()', 'l'),
            ('位置', '//div[@id="list"]//table//tbody//tr//td[4]//a//text()', 'l'),
            ('运营商', '//div[@id="list"]//table//tbody//tr//td[5]//a//text()', 'l'),
            ('响应速度', '//div[@id="list"]//table//tbody//tr//td[6]//text()', 'l'),
            ('最后验证时间', '//div[@id="list"]//table//tbody//tr//td[7]//text()', 'l'),
            ('存活时间', '//div[@id="list"]//table//tbody//tr//td[8]//text()', 'l'),
        ]
        #list = rule.html_content_analysis_row(html_text=list_html, column=colum, url=url[0])
        #print(list)
        for row_html in row_html:
            row = rule.html_content_analysis_list(row_html=row_html, column=colum, url=url[0])
            print(row)
            #sql = "insert into ip (IP,端口,匿名度,类型,位置,运营商,响应速度,最后验证时间,存活时间) value('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (row[0][1], row[1][1], row[2][1], row[3][1], row[4][1], row[5][1], row[6][1], row[7][1], row[8][1])
            #print(sql)
            # ldae_mysql.write_sql(sql=sql)
            # th = threading.Thread(target=read_detial, args=(a,str))
            # th.start()  # 启动线程
        next_url = (url[0].replace('%d.shtml' % (page), '%d.shtml' % (page + 1)), url[1])
        page = page + 1
        if page < 369:
            list_detail(next_url, page)
    else:
        return


if __name__ == '__main__': # 判断文件入口
    main()
