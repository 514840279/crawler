# -- coding: UTF-8 --

from common.HtmlSource import HtmlSource
from common.Rule import Rule
#from common.inc_conn import Conn_mysql
from common.inc_csv import Csv_base
from common.inc_file import File_file,File_floder
import requests
from lxml import html

floder = File_floder()
htmlSource = HtmlSource()
rule = Rule()
csv = Csv_base()
flag =0
commontitle = 1

# 多线程
def read_detial(url,path):
    if(str(url[0][1]).startswith("http") and url[1][1]!="收起"):
        # TODO 翻页
        for i in range(1,11):
            print(url[0][1])
            detial_html = htmlSource.get_html(url_p=url[0][1]+"/?page=%d" % i, type_p='rg')
            tree = html.fromstring(detial_html)
            hreflist = tree.xpath('//ul[@class="list"]/li/div/div/p[@class="name"]/a/@href')
            if len(hreflist)>0:
                for href in hreflist:
                    save_context('http://www.xiachufang.com'+href,url[1][1],path)


def save_context(url,type,path):
    print(url,type,path)
    colum = [
        ('分类', type, 'n'),
        ('地址', url, 'n'),
        ('名称', '//h1[@class="page-title"]/text()', 'l'),
        ('图片', '//div[@class="block recipe-show"]/div[@class="cover image expandable block-negative-margin"]/img/@src', 'l'),
        ('综合评分', '//div[@class="block recipe-show"]//div[@class="score float-left"]/span[@class="number"]/text()', 'l'),
        ('人做过这道菜', '//div[@class="block recipe-show"]//div[@class="cooked float-left"]/span[@class="number"]/text()', 'l'),
        ('作者', '//div[@class="block recipe-show"]/div[@class="author"]/a/span[@itemprop="name"]/text()', 'l'),
        ('作者主页', '//div[@class="block recipe-show"]/div[@class="author"]/a/@href', 'sab','http://www.xiachufang.com'),
        ('作者头像', '//div[@class="block recipe-show"]/div[@class="author"]/a/img/@src', 'l'),
        ('菜描述', '//div[@class="block recipe-show"]/div[@class="desc mt30"]//text()', 'sarr'),
        ('用料', '//div[@class="block recipe-show"]/div[@class="ings"]/table//text()', 'sab',''),
        ('做法', '//div[@class="block recipe-show"]/div[@class="steps"]/ol/li//text()', 'sab',''),
        ('做法图片', '//div[@class="block recipe-show"]/div[@class="steps"]/ol/li//img//@src',  'sab', ''),

    ]

    global commontitle
    if (commontitle == 0):
        str_t = []
        commontitle = 1
        for i in range(0, len(colum)):
            str_t.append(colum[i][0])
        csv.write_csv_file_line(file_path=path+"_context.csv", str=str_t)

    detial_html = htmlSource.get_html(url_p=url, type_p='rg')
    result = rule.html_content_analysis_detial(html_text=detial_html, column=colum, url=url)
    print(str(result))
    str_t = []
    for row in result:
        str_t.append(str(row[1]))
        if (row[0] == '做法图片'):
            save_img(imgs=row[1],path=path)
    csv.write_csv_file_line(file_path=path+"_context.csv", str=str_t)


def save_img(imgs,path):
    for img_url in imgs:
        img_content = requests.get(img_url).content
        if(img_url.find(".jpg")>-1):
            img_name = img_url[0:img_url.find(".jpg")]
            img_name = img_name.split('/')[-1]+".jpg"
        if (img_url.find(".png") > -1):
            img_name = img_url[0:img_url.find(".png")]
            img_name = img_name.split('/')[-1] + ".png"
        if (img_url.find(".jpeg") > -1):
            img_name = img_url[0:img_url.find(".jpeg")]
            img_name = img_name.split('/')[-1] + ".jpeg"
        if (img_url.find(".gif") > -1):
            img_name = img_url[0:img_url.find(".gif")]
            img_name = img_name.split('/')[-1] + ".gif"
        print(img_name)
        with open(path+'/%s' % img_name, 'wb') as f:
            f.write(img_content)

# 多页
def main():

    path = '../data/xiachufang'

    floder.add(path_p=path)

    url = "http://www.xiachufang.com/category/"
    list_html = htmlSource.get_html(url_p=url, type_p='rg')
    colum = [('href', '//div[@class="block-bg p40 font16"]//div[@class="cates-list-all clearfix hidden"]//a/@href', 'sab','http://www.xiachufang.com'),
             ('name', '//div[@class="block-bg p40 font16"]//div[@class="cates-list-all clearfix hidden"]//a/text()', 'l')]
    list = rule.html_content_analysis_list(html_text=list_html, column=colum, url=url)


    for i in range(0,len(list)):
        #print(list[i])
        read_detial(list[i],path)



if __name__ == '__main__': # 判断文件入口
    main()
