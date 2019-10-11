# -- coding: UTF-8 --


import requests
from lxml import etree
from common.inc_file import File_file

file = File_file()
urlx = 'https://jieqi.supfree.net/cntv.asp?n='
session = requests.Session()

for year in range(833,5001):
    dicall = {}
    url = urlx+str(year)
    resp = session.get(url=url)
    resp.encoding = 'gb2312'
    rep = etree.HTML(resp.text)
    a = rep.xpath('//table/tr/td/a/text()')
    b = rep.xpath('//table/tr/td/text()')
    dicall[str(year)]={}
    for i in range(len(a)):
        if len(b) >i:
            dicall[str(year)][a[i]] = str(b[i]).strip()[:-9]
    file.save_source(path="./",file="jieqi.json",all_the_text=str(dicall)+"\n")