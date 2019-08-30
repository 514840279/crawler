#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# develop 514840279
#-----系统自带必备模块引用-----

import requests
import re #正则处理
import urllib
import chardet
from urllib import parse
from bs4 import BeautifulSoup as bs_4
from selenium import webdriver # 浏览器引擎webdriver模块
from lxml import etree
import json
import os
from selenium.webdriver.chrome.options import Options 

# 获取网页源码 重要
class HtmlSource:
    def get_html(self,url_p, type_p='rp', charset_p='utf-8',timeout_p=10,post_data='',headers_p={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}):
        txt = "nothing"
        # 获取网页源码
        try:
            # get的方法
            if type_p == 'rg':
                html_content = requests.get(url=url_p, timeout=timeout_p, headers=headers_p)
                txt = str(html_content.text.encode(encoding=html_content.encoding,errors='ignore'), encoding=charset_p,errors='ignore')
            # post的方法
            if type_p == 'rp':
                if post_data != '':
                    html_content = requests.post(url=url_p,data=json.dumps(post_data), timeout=timeout_p, headers=headers_p)
                    txt = str(html_content.text.encode(encoding=html_content.encoding, errors='ignore'), encoding=charset_p,errors='ignore')
                    html_content.close()
                else:
                    html_content = requests.post(url=url_p, timeout=timeout_p, headers=headers_p)
                    txt = str(html_content.text.encode(encoding=html_content.encoding,errors='ignore'), encoding=charset_p,errors='ignore')
                    html_content.close()

            # session的方法
            if type_p == 'ss':
                res_addr = self.session.get(url_p, timeout=timeout_p, headers=headers_p)
                res_addr.encoding = chardet.detect(res_addr.content)["encoding"]
                txt = bs_4(res_addr.text, "lxml")

            # urllib的方法
            if type_p == 'ul':
                html_content = urllib.request.urlopen(url=url_p)
                txt = html_content.read().decode(charset_p, "ignore")
                html_content.close()

            # Selenium的方法 待完善
            if type_p == 'se':
                self.driver.get(url_p)
                js = "var q=document.body.scrollTop=100000"
                self.driver.execute_script(js)
                self.driver.implicitly_wait(30)  # 据说此方法是智能等待，看效果还不错，数据加载完就返回了 30 代表等待秒
                txt = self.driver.page_source

        except Exception as e:
            print(e.args)
            raise e
        return txt

    #  获取网页原文 （ulib）
    def get_html_ulib(self,url_p, type_p='rp', chartset_p='utf-8'):
        html = urllib.request.urlopen(url=url_p)
        txt = html.read().decode(chartset_p)
        html.close()
        return txt

    #  获取网页原文 （selenium）
    def get_html_selenium(self,url_p):
        driver = webdriver.Chrome("../driver/chromedriver.exe")

        driver.get(url_p)
        js = "document.documentElement.scrollTop=1000000"
        driver.execute_script(js)
        driver.implicitly_wait(30)  # 据说此方法是智能等待，看效果还不错，数据加载完就返回了 30 代表等待秒
        print(driver)
        txt = driver.page_source
        return txt,driver

    # 获取网页字符集
    def get_encodings_from_content(self,content):
        charset = re.compile(r'<meta.*?charset=["\']*(.+?)["\'>]', flags=re.I).findall(content)
        if len(charset) == 0:
            charset = re.compile(r'<meta.*?content=["\']*;?charset=(.+?)["\'>]', flags=re.I).findall(content)
            if len(charset) == 0:
                charset = re.compile(r'^<\?xml.*?encoding=["\']*(.+?)["\'>]').findall(content)
                if len(charset) == 0:
                    charset = ['utf-8']
        return charset[0]


if __name__ == '__main__':
    print("")