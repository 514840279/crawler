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
commontitle = 0
#ldae_mysql = Conn_mysql( host='localhost', user='root', passwd='root', db='ldae', port=3306) # 生成MYSQL数据库索引数据实例

# 多线程
def read_detial(url,path):
    detial_html = htmlSource.get_html(url_p=url, type_p='rg')

    #save_menu(url,detial_html = detial_html,path)
    tree = html.fromstring(detial_html)
    li = tree.xpath('//div[@class="cp_comlist_w"]/ul[@class="clearfix"]/li')
    if len(li)>0:
        save_commons(url,detial_html,path)

def save_menu(url,detial_html,path):
    #print(detial_html)
    global flag
    colum = [
        ('地址', url, 'n'),
        ('标题', '//a[@id="tongji_title"]//text()', 'l'),
        #('收藏', '//div[@class="info1"]//span[@class="favbtns"]//span//text()', 'l'),
        ('标签', '//dl[@class="yj_tags clearfix"]//text()', 'l'),
        ('工艺', '//a[@id="tongji_gy"]//text()', 'l'),
        ('难度', '//a[@id="tongji_nd"]//text()', 'l'),
        ('人数', '//a[@id="tongji_rsh"]//text()', 'l'),
        ('口味', '//a[@id="tongji_kw"]//text()', 'l'),
        ('准备时间', '//a[@id="tongji_zbsj"]//text()', 'l'),
        ('烹饪时间', '//a[@id="tongji_prsj"]//text()', 'l'),
        ('作者', '//a[@id="tongji_author"]//text()', 'l'),
        ('主料', '//div[@class="yl zl clearfix"]//ul//li//div//h4//text()', 'l'),
        ('辅料', '//div[@class="yl fuliao clearfix"]//ul//li//text()', 'l'),
        ('做法', '//div[@class="editnew edit"]//text()', 'sarr-reg', r'swiper-container1.*?}\);'),
        ('图片', '//div[@class="editnew edit"]//img//@src', 'sab', ''),

    ]
    str_t = []
    if(flag == 0):
        for i in range(0, len(colum)):
            str_t = str_t.append(str(colum[i][0]))
        csv.write_csv_file_line(file_path=path+".csv", str=str_t)
        flag = 1

    result = rule.html_content_analysis_detial(html_text=detial_html, column=colum, url=url)
    print(str(result))
    str_t = []
    # 写入文件
    for i in range(0,len(colum)):
        str_t = str_t.append(str(result[i][1]))
        if(colum[i][0]=='图片'):
            save_img(imgs=result[i][1])
    csv.write_csv_file_line(file_path=path+".csv",str=str_t)
    #print(result)
    #sql="insert into cancer value('%s','%s','%s','%s','%s')"%(result[0][1][0],str(result[1][1][0]).replace('患者,图片因隐私问题无法显示','').replace("患者,","患者:").replace("医生,","医生:").replace('\'','"'),type,'春雨医生',url)
    #print(sql)
    #ldae_mysql.write_sql(sql=sql)

def save_commons(url,detial_html,path):

    colum = [
        ('地址', url, 'n'),
        ('昵称', '//div[@class="cp_comlist_w"]/ul[@class="clearfix"]/li/a/h5/text()', 'l'),
        ('用户头像', '//div[@class="cp_comlist_w"]/ul[@class="clearfix"]/li/a/img/@src', 'l'),
        ('用户主页', '//div[@class="cp_comlist_w"]/ul[@class="clearfix"]/li/a/@href', 'l'),
        ('评论内容', '//div[@class="cp_comlist_w"]/ul[@class="clearfix"]/li/div[@class="c"]/p[@class="p1"]/text()', 'arr',1),
        ('评论时间', '//div[@class="cp_comlist_w"]/ul[@class="clearfix"]/li/div[@class="c"]/div[@class="info"]/span[1]/text()', 'arr-replace','来自'),
        ('回复数', '//div[@class="cp_comlist_w"]/ul[@class="clearfix"]/li/div[@class="c"]/div[@class="info"]/span[@class="zzzzan"]/strong/text()', 'l'),

    ]

    global commontitle
    if (commontitle == 0):
        str_t = []
        commontitle = 1
        for i in range(0, len(colum)):
            str_t.append(colum[i][0])
        csv.write_csv_file_line(file_path=path+"_common.csv", str=str_t)


    result = rule.html_content_analysis_list(html_text=detial_html, column=colum, url=url)
    print(str(result))
    for row in result:
        str_t = []
        # 写入文件
        for i in range(0, len(colum)):
            str_t.append(str(row[i][1]))
        csv.write_csv_file_line(file_path=path+"_common.csv", str=str_t)


def save_img(imgs,path):
    for img_url in imgs:
        img_content = requests.get(img_url).content
        with open(path+'/%s' % img_url.split('/')[-1], 'wb') as f:
            f.write(img_content)

# 多页
def main():

    path = '../data/meishij'

    list_menu =csv.read_csv_file(path+"_menu.csv")
    print(list_menu)
    # 创建文件夹

    floder.add(path_p=path)
    for i in range(0,len(list_menu)):
        print(list_menu[i])
        if(i>0):
            start_url = list_menu[i][0]+"?&page=%d"
            for i in range(1,int(list_menu[i][2])+1):
                url = start_url%(i)
                print(url)
                list_html = htmlSource.get_html(url_p=url,type_p='rg')

                #print(list_html)
                colum=[('a','//div[@class="listtyle1_w"]//div[@class="listtyle1_list clearfix"]//div[@class="listtyle1"]//a//@href','l')]
                list = rule.html_content_analysis_detial(html_text=list_html,column=colum,url=url)
                print(list)
                for a in list[0][1]:
                    read_detial(a,path)
                    #th = threading.Thread(target=read_detial, args=(a,str))
                    #th.start()  # 启动线程


if __name__ == '__main__': # 判断文件入口
    main()
