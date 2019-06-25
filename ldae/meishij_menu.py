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
csv = Csv_base()
menu_list=[]
path = '../data/meishij'
# 多页
def main():

    start_menu=['/chufang/diy/','/jiankang/']
    start_url = "https://www.meishij.net%s"
    str_t = ['地址', '文本', '页数']
    csv.write_csv_file_line(file_path=path + "_menu.csv", str=str_t)

    for menu in start_menu:
        url = start_url%menu
        html_source=htmlSource.get_html(url_p=url,type_p='rg')
        tree = html.fromstring(html_source)

        # 当前分类
        list_a = tree.xpath('*//ul[@class="listnav_ul"]/li/h1/a')
        for a in list_a:
            sub_url = a.xpath('./@href')[0]
            sub_text = a.xpath('./text()')[0]
            add_list(sub_url, sub_text)
            print(sub_url,sub_text)

        # 其他分类
        list_b = tree.xpath('*//ul[@class="listnav_ul"]/li/a')
        for a in list_b:
            sub_url = a.xpath('./@href')
            sub_text=a.xpath('./text()')[0]
            print(sub_url, sub_text)
            if(len(sub_url)>0):
                if(str(sub_url[0]).startswith("http")):
                    url_t = sub_url[0]
                else:
                    url_t = start_url%sub_url[0]
                print(url_t)
                add_list(sub_url =url_t,sub_text= sub_text)
                html_source_t = htmlSource.get_html(url_p=url_t, type_p='rg')
                tree_t = html.fromstring(html_source_t)
                # 其他小分类
                list_d = tree_t.xpath('*//div[@class="other_c listnav_con clearfix"]/dl/dd/a')
                for a in list_d:
                    sub_url = a.xpath('./@href')[0]
                    sub_text = a.xpath('./text()')[0]
                    print(sub_url,sub_text)
                    add_list(sub_url, sub_text)

        # 当前小分类
        list_c = tree.xpath('*//div[@class="listnav_con clearfix"]/dl/dd/a')
        for a in list_c:
            sub_url = a.xpath('./@href')[0]
            sub_text = a.xpath('./text()')[0]
            add_list(sub_url, sub_text)


        print(menu_list)

def add_list(sub_url,sub_text):
    html_source = htmlSource.get_html(url_p=sub_url, type_p='rg')
    tree = html.fromstring(html_source)
    text = tree.xpath('*//div[@class="listtyle1_page_w"]/span/form/text()')
    print(text,sub_text)
    if (len(text)>0):
        text = text[0]
        pageSize = str(text).replace('共', '').replace('页，到第 ', '')
        menu_list.append({"url": sub_url, "title": sub_text, "maxPageSize": pageSize})
        str_t=[sub_url,sub_text,pageSize]
        csv.write_csv_file_line(file_path=path + "_menu.csv", str=str_t)



if __name__ == '__main__': # 判断文件入口
    main()
