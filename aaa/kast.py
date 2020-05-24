# -- coding: UTF-8 --

from common.HtmlSource import HtmlSource
from common.Rule import Rule
#from common.inc_conn import Conn_mysql
from common.inc_csv import Csv_base
from common.inc_file import File_file,File_floder
import requests
from lxml import html
import time


floder = File_floder()
htmlSource = HtmlSource()
rule = Rule()
csv = Csv_base()
flag =0
commontitle = 1

# 多线程
def save_html(content,url):
    html_name='hanguo'
    type(content)
    with open("D://html" + '/%s' %html_name, 'a+b') as f:
        f.write(content)
        f.write(b"***********************************************\n")


def read_detial(url,driver):
    print(url[0][1])
    detial_html,driver = htmlSource.get_html_selenium(url_p=url[0][1],driver=driver)
    tree = html.fromstring(detial_html)
    content = tree.xpath('//section[@id="content"]')
    print(html.tostring(content[0]))
    save_html(html.tostring(content[0]),url[0][1])
    print(url[1][1])
    #save_img([url[1][1]],"D://img")




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
        if (img_url.find(".bmp") > -1):
            img_name = img_url[0:img_url.find(".bmp")]
            img_name = img_name.split('/')[-1] + ".bmp"
        print(img_name)
        with open(path+'/%s' % img_name, 'wb') as f:
            f.write(img_content)

# 多页
def main():
    driver=None
    for a in range(27,28):
        print("page=%d" %a)
        url = "https://kast.or.kr/en/member/info.php?start=%d&n=%d" %((a-1)*24,((a-1)*10)+1)
        print(url)
        list_html,driver = htmlSource.get_html_selenium(url_p=url,driver=None)
        colum = [('href', '//ul[@class="member-list"]//li//a/@href', 'sab','https://kast.or.kr/en/member/'),
                 ('img', '//ul[@class="member-list"]//li//a/div/span/img/@src', 'sab','https://kast.or.kr/'),
                 ('name', '//ul[@class="member-list"]//li//a/div[@class="member-info-box"]/p/text()', 'l'),]

        list = rule.html_content_analysis_list(html_text=list_html, column=colum, url=url)
        print(list)
        #
        # flag = False
        for i in range(0,len(list)):
            read_detial(list[i],driver)






if __name__ == '__main__': # 判断文件入口

    main()
