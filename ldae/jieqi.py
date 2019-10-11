# -- coding: UTF-8 --


import requests
from lxml import etree
from common.inc_file import File_file

file = File_file()
urlx = 'https://jieqi.supfree.net/cntv.asp?n='
session = requests.Session()
dicall={}
for year in range(1,5001):
    url = urlx+str(year)
    resp = session.get(url=url)
    resp.encoding = 'gb2312'
    rep = etree.HTML(resp.text)
    a = rep.xpath('//table/tr/td/a/text()')
    b = rep.xpath('//table/tr/td/text()')
    dicall[str(year)]={}
    for i in range(len(a)):
        dicall[str(year)][a[i]] = str(b[i]).strip()[:-9]
file.save_source(file="jieqi.json",all_the_text=dicall)