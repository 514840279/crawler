# -- coding: UTF-8 --
from common.HtmlSource import HtmlSource

htmlSource = HtmlSource()

url = 'https://www.meishij.net/zuofa/hubeixianroutangyuan.html'
html_source = htmlSource.get_html(url_p=url)
print(html_source)

detial_html = htmlSource.get_html(url_p=url, type_p='rg')
print(detial_html)