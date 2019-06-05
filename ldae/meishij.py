# -- coding: UTF-8 --

from common.HtmlSource import HtmlSource
from common.Rule import Rule
#from common.inc_conn import Conn_mysql
from common.inc_csv import Csv_base


htmlSource = HtmlSource()
rule = Rule()
csv = Csv_base()
flag =0
#ldae_mysql = Conn_mysql( host='localhost', user='root', passwd='root', db='ldae', port=3306) # 生成MYSQL数据库索引数据实例

# 多线程
def read_detial(url):
    detial_html = htmlSource.get_html(url_p=url, type_p='rg')
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
    str_t = ''
    if(flag == 0):
        for i in range(0, len(colum)):
            if (i > 0):
                str_t = str_t + ','
            str_t = str_t + "`" + str(colum[i][0]) + "`"
        csv.write_csv_file_line(file_path="../data/meishij.csv", str=[str_t])
        flag = 1

    result = rule.html_content_analysis_detial(html_text=detial_html, column=colum, url=url)
    print(str(result))
    str_t = ''
    # 写入文件
    for i in range(0,len(colum)):
        if(i>0):
            str_t = str_t+','
        str_t = str_t+"`"+str(result[i][1])+"`"
    csv.write_csv_file_line(file_path="../data/meishij.csv",str=[str_t])
    #print(result)
    #sql="insert into cancer value('%s','%s','%s','%s','%s')"%(result[0][1][0],str(result[1][1][0]).replace('患者,图片因隐私问题无法显示','').replace("患者,","患者:").replace("医生,","医生:").replace('\'','"'),type,'春雨医生',url)
    #print(sql)
    #ldae_mysql.write_sql(sql=sql)

# 多页
def main():
    start_url = "https://www.meishij.net/chufang/diy/zaocan/?&page=%d"



    for i in range(1,57):
        url = start_url%(i)
        print(url)
        list_html = htmlSource.get_html(url_p=url,type_p='rg')

        #print(list_html)
        colum=[('a','//div[@class="listtyle1_w"]//div[@class="listtyle1_list clearfix"]//div[@class="listtyle1"]//a//@href','l')]
        list = rule.html_content_analysis_detial(html_text=list_html,column=colum,url=url)
        print(list)
        for a in list[0][1]:
            read_detial(a)
            #th = threading.Thread(target=read_detial, args=(a,str))
            #th.start()  # 启动线程





if __name__ == '__main__': # 判断文件入口
    main()
