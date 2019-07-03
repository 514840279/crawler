# -- coding: UTF-8 --

from common.HtmlSource import HtmlSource
from common.Rule import Rule
from common.inc_file import File_file,File_floder
from common.inc_csv import Csv_base
import requests
from lxml import html

floder = File_floder()
file =File_file()
htmlSource = HtmlSource()
rule = Rule()
csv = Csv_base()
flag =0

# 多页
def main():
    global  flag
    # 百度百科
    start_url = "https://www.baidu.com/s?wd=%s site:baike.baidu.com&pn=0&rn=50&ie=utf-8"

    # 读取文件
    lines =csv.read_csv_file(file_path='百科候选关键词.txt')
    print(lines)

    # 创建文件夹
    path = '../data/百科候选关键词'
    floder.add(path_p=path)

    cont = False
    for line in range(1,len(lines)):
        if(len(lines[line])>0):
            if(lines[line][0] == '龙骨'):
                cont = True
            if cont:
                url = start_url%(lines[line][0])
                print(url)
                html_text = htmlSource.get_html(url_p=url,type_p='rg')
                #print(list_html)
                group=[('row','//div[@id="content_left"]/div','l')]
                colum=[('keyword',lines[line][0],'n'),
                       ('srcid','1599','n'),
                       ('标题','./h3/a//text()','l'),
                       ('网址','./h3/a/@href','l'),
                       ('图片','.//div[@class="general_image_pic c-span6"]/a[@class="c-img6"]/img/@src','l'),
                       ('简介','.//div[@class="c-abstract"]//text()','sarr'),
                       ('日期', './/div[@class="c-abstract"]/span[@class=" newTimeFactor_before_abs m"]/text()', 'l'),
                       ('标签', '', 'n'),
                       ('标签地址', '', 'n'),
                       ('来源', './/div[@class="f13"]/a[@class="c-showurl"]/span/text()', 'l'),
                       ('快照', './/div[@class="f13"]/a[@class="m"]/@href', 'l'),
                       ]

                colum2=[('keyword',lines[line][0],'n'),
                        ('srcid','1547','n'),
                        ('标题','./h3/a//text()','l'),
                        ('网址','./h3/a/@href','l'),
                        ('图片','.//div[@class="c-span6"]/a/img/@src','l'),
                        ('简介','.//div[@class="c-span18 c-span-last"]/p[1]//text()','sarr'),
                        ('日期', '', 'n'),
                        ('标签','.//div[@class="c-span18 c-span-last"]/p[1]/a/text()','arr'),
                        ('标签地址','.//div[@class="c-span18 c-span-last"]/p[1]/a/@href','arr'),
                        ('来源', './/div[@class="c-span18 c-span-last"]/span[1]/text()', 'l'),
                        ('快照', '', 'n'),
                       ]
                str_t = []
                if (flag == 0):
                    for i in range(0, len(colum)):
                        str_t.append("`"+colum[i][0]+"`")
                    str_t.append("`本地路径`")
                    csv.write_csv_file_line(file_path=path+".csv", str=str_t)
                    flag = 1

                tree = html.fromstring(html_text)
                list = rule._analysis_(tree=tree, column=group,url=url)
                lista =[]
                for a in range(len(list[0][1])):
                    tree_t = list[0][1][a]
                    try:
                        srcid = tree_t.xpath('@srcid')[0]
                        if srcid=='1547':
                            row = rule._analysis_(tree=list[0][1][a], column=colum2, url=url)
                            lista.append(row)
                        elif srcid == '1599':
                            row = rule._analysis_(tree=list[0][1][a], column=colum, url=url)
                            lista.append(row)
                    except Exception:
                        print("no srcid")
                for row in lista:
                    try:
                        text = ''
                        for st in  row[2][1]:
                            text = text+str(st).strip()
                        if text.index(lines[line][0])>-1:
                            str_t = []
                            # 写入文件
                            file_path =''
                            for i in range(0, len(colum)):
                                str_t.append("`"+"".join(row[i][1])+"`")
                                if (colum[i][0] == '网址'):
                                    url = row[i][1][0]
                                    html_text = htmlSource.get_html(url_p=url, type_p='rg')
                                    file_name = str(url).replace("http://www.baidu.com/link?url=", '')
                                    file.save_source(path=path, file=file_name+".html", all_the_text=html_text)
                                    file_path = path+'/%s'%file_name
                            str_t.append("`"+ file_path+"`")
                            csv.write_csv_file_line(file_path=path+".csv", str=str_t)
                    except Exception:
                        print(row[2][1],lines[line][0],False)

                    #th = threading.Thread(target=read_detial, args=(a,str))
                    #th.start()  # 启动线程


if __name__ == '__main__': # 判断文件入口
    main()
