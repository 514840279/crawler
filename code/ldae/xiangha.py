# -- coding: UTF-8 --

from common.HtmlSource import HtmlSource
from common.Rule import Rule
from common.inc_conn import Conn_mysql
from common.inc_csv import Csv_base
import time

htmlSource = HtmlSource()
rule = Rule()
csv = Csv_base()
flag =0
#ldae_mysql = Conn_mysql( host='localhost', user='root', passwd='root', db='ldae', port=3306) # 生成MYSQL数据库索引数据实例

# 多线程
def read_detial(url):
    time.sleep(3)
    detial_html = htmlSource.get_html(url_p=url, type_p='rg')
    #print(detial_html)
    global flag
    colum=[
        ('标题','//div[@class="rec_content"]//h2//text()','l'),
        ('图片','//div[@class="rec_content"]//div[@class="rec_pic"]//div[@class="pic"]//img//@src','l'),
        ('浏览', '//div[@class="rec_content"]//div[@class="rec_social clearfix"]//div[@class="info"]//text()', 'arr',0),
        ('收藏', '//div[@class="rec_content"]//div[@class="rec_social clearfix"]//div[@class="info"]//span[@id="j_show_favorite"]//text()', 'l'),
        ('作者', '//div[@class="rec_content"]/div[@class="dish_author"]//a//text()', 'l'),
        ('健康功效', '//div[@class="rec_content"]//div[@class="rec_hea"]//p//text()', 'l'),
        ('食材用料', '//div[@class="rec_content"]//div[@class="rec_ing"]//table//tr//td//div[@class="cell"]//text()', 'arr-replace','相克食物'),
        ('做法', '//div[@class="rec_content"]//div[@class="step_con"]//ul[@id="CookbookMake"]//li//p//text()', 'sab',''),
        ('步骤图片', '//div[@class="rec_content"]//div[@class="step_con"]//ul[@id="CookbookMake"]//li//img//@src', 'sab', ''),

   ]
    str_t = ''
    if (flag == 0):
        for i in range(0, len(colum)):
            if (i > 0):
                str_t = str_t + ','
            str_t = str_t + "`" + str(colum[i][0]) + "`"
        csv.write_csv_file_line(file_path="../data/xiangha.csv", str=[str_t])
        flag = 1

    result = rule.html_content_analysis_detial(html_text=detial_html, column=colum, url=url)
    print(str(result))
    str_t = ''
    # 写入文件
    for i in range(0, len(colum)):
        if (i > 0):
            str_t = str_t + ','
        str_t = str_t + "`" + str(result[i][1]) + "`"
    csv.write_csv_file_line(file_path="../data/xiangha.csv", str=[str_t])
    #print(result)
    #sql="insert into cancer value('%s','%s','%s','%s','%s')"%(result[0][1][0],str(result[1][1][0]).replace('患者,图片因隐私问题无法显示','').replace("患者,","患者:").replace("医生,","医生:").replace('\'','"'),type,'春雨医生',url)
    #print(sql)
    #ldae_mysql.write_sql(sql=sql)

# 多页
def main():
    start_url = "https://www.xiangha.com/caipu/c-zaocan/hot-%d"

    for i in range(33,437):
        url = start_url%(i)
        print(url)
        list_html = htmlSource.get_html(url_p=url,type_p='rg')

        #print(list_html)
        colum=[('a','//div[@class="s_list"]//ul//li//a[@class="pic "]//@href','l')]
        list = rule.html_content_analysis_detial(html_text=list_html,column=colum,url=url)
        print(list)
        for a in list[0][1]:
            read_detial(a)
            #th = threading.Thread(target=read_detial, args=(a,str))
            #th.start()  # 启动线程





if __name__ == '__main__': # 判断文件入口
    main()
