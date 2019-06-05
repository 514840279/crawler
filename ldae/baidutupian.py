#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.HtmlSource import HtmlSource
from common.Rule import Rule
from common.inc_conn import Conn_mysql
import re,time



htmlSource = HtmlSource()
rule = Rule()
ldae_mysql = Conn_mysql( host='localhost', user='root', passwd='514840279@qq.com', db='application', port=3306) # 生成MYSQL数据库索引数据实例

# 从主页获取斗图的每一个url 获取源码
def get_img_html(html):
    soup = BeautifulSoup(html,'lxml') # c创建一个对象
    all_a=soup.find_all('a',class_="list-group-item") # 过滤 下划线 class_ 区分关键字
    for i in all_a:
        img_html = get_html(i['href'])#找到超链接
        # print img_html
        get_img(img_html)

# 获取每个图片
def get_img(html):
    soup = etree.HTML(html) # 初始化打印源码，自动补全
    items = soup.xpath('//div[@class="artile_des"]') # 解析网页方法 // 选择 ， 【】 条件， @
    for item in items:
        imgurl = item.xpath('table/tbody/tr/td/a/img/@onerror')
        start_save_img(imgurl)

# 下载图片
def save_img(img_url):
    img_url = img_url.split('=')[-1][1:-2].replace('jp','jpg')
    print ('正在下载'+'http:'+img_url)
    img_content = requests.get('http:'+img_url).content
    with open('doutu/%s.jpg'% img_url.split('/')[-1],'wb') as f:
        f.write(img_content)

# 多线程
def  start_save_img(imgurl_list):
    for i in imgurl_list:
        th = threading.Thread(target=save_img,args=(i,))
        th.start() # 启动线程


def saveHtml( file_content):
    #    注意windows文件命名的禁用符，比如 /
    with open( "1.html", "wb") as f:
        #   写文件用bytes而不是str，所以要转码
        f.write(file_content.encode())

# 多页
def main():
    url = "https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gb18030&word=%B2%A1%C0%ED%B1%A8%B8%E6&fr=ala&ala=1&alatpl=adress&pos=0&hs=2&xthttps=111111"
    #https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1534733085751_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&hs=2&word=%E7%97%85%E7%90%86%E6%8A%A5%E5%91%8A
    #ttps://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&fm=detail&lm=-1&st=-1&sf=2&fmq=1534732696173_R_D&fm=detail&pv=&ic=0&nc=1&z=&se=&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&hs=2&word=%E7%97%85%E7%90%86%E6%8A%A5%E5%91%8A
    #https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1534733085751_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&hs=2&word=%E7%97%85%E7%90%86%E6%8A%A5%E5%91%8A
    #https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&fm=index&pos=history&word=%E7%97%85%E7%90%86%E6%8A%A5%E5%91%8A
    #str = ["肺癌"," 肝癌","乳腺癌","胃癌","直肠癌"] 

    list_html,driver = htmlSource.get_html_selenium(url_p=url)
    for a in range(1,100) :
        js = "document.documentElement.scrollTop=1000000000000000000000000000000000000"
        driver.execute_script(js)
        pic_url = re.findall('"objURL":"(.*?)",', driver.page_source, re.S)
        # imgpage = driver.find_element_by_xpath('//div[@class="imgpage"]').get_attribute("thumburl")
        print(pic_url)
    time.sleep(30000)



    #saveHtml(file_content=list_html)
    #colum=[('imglist','//div[@class="imgpage"]//ul//li[@class="imgitem"]//@thumburl','l')]
    #list = rule.html_content_analysis_detial(html_text=list_html,column=colum,url=url)
    #print(list)
    #for a in list[0][1]:
    #    read_detial(a, ss)
        #th = threading.Thread(target=read_detial, args=(a,str))
        #th.start()  # 启动线程


if __name__ == '__main__': # 判断文件入口
    
    main()
