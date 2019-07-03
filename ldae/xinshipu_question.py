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
#ldae_mysql = Conn_mysql( host='localhost', user='root', passwd='root', db='ldae', port=3306) # 生成MYSQL数据库索引数据实例

# 多线程
def read_detial(url,path,question_colum,aswer_column):
    if(str(url).startswith("http")):
        detial_html = htmlSource.get_html(url_p=url, type_p='rg')

        #save_menu(url,detial_html = detial_html,path)

        colum = [('a', '*//ul[@class="table-list"]/li/div[@class="fl w410"]/a/@href', 'sab','https://www.xinshipu.com'),
                 ('page','*//div[@class="paging mt20"]//a[@class="next-page"]/@href','sab','https://www.xinshipu.com')]

        result = rule.html_content_analysis_detial(column=colum, html_text=detial_html, url='https://www.xinshipu.com')
        print(result)

        for a in result[0][1]:
            read_question(a,path,question_colum,aswer_column)


        next_page = result[1][1]
        print(next_page)
        if len(next_page)>0:
            read_detial(next_page[0],path,question_colum,aswer_column)



def read_question(url,path,question_colum,aswer_column):

    detial_html = htmlSource.get_html(url_p=url, type_p='rg')

    # 解决问题
    result = rule.html_content_analysis_detial(column=question_colum, html_text=detial_html, url='https://www.xinshipu.com')
    print(result)
    save_question(result,url,path)

    # 解决评论
    if(len(result[5][1])>0):
        group=[('a','*//div[@class="qa-answer-list"]/div[@class="qa-aswer"]','l')]
        li =rule.html_content_analysis_list2(html_text=detial_html,group=group,column=aswer_column,url='https://www.xinshipu.com')

        save_commons(li,url,path)



def save_question(result,url,path):
    str_t = []
    for i in range(0, len(result)):
        if(len(result[i][1])>0):
            str_t.append(result[i][1][0])
        else:
            str_t.append('')
    str_t.append(url)
    csv.write_csv_file_line(file_path=path + "/question.csv", str=str_t)


def save_commons(li,url,path):
    for result in li:
        str_t = []
        for i in range(0, len(result)):
            if (len(result[i][1]) > 0):
                str_t.append(result[i][1][0])
            else:
                str_t.append('')
        str_t.append(url)
        print(result)
        csv.write_csv_file_line(file_path=path + "/aswer.csv", str=str_t)


# 多页
def main():
    path = '../data/xinshipu'
    # 创建文件夹
    floder.add(path_p=path)
    start_url = "https://www.xinshipu.com/question"

    # 问题结构
    question_colum = [('网友/ip', '*//div[@class="bpannel"]//a[@class="cb"]/span/text()', 'l'),
                      ('网友主页', '*//div[@class="bpannel"]//a[@class="cb"]/@href', 'sab', 'https://www.xinshipu.com'),
                      ('小头像', '*//div[@class="bpannel"]//a[@class="cb"]/img[@class="portrait-small"]/@src', 'sab',
                       'https:'),
                      ('关注', '*//div[@class="bpannel"]//span[@class="ml4"]/text()', 'l'),
                      ('浏览', '*//div[@class="bpannel"]//div[@class="fr font2 cg2"]/span[2]/text()', 'l'),
                      ('回答', '*//div[@class="qa-title font16 cg1"]/span[@class="col"]/text()', 'l'),
                      ('问题', '*//div[@class="bpannel"]//div[@class="p20"]/p[@class="font16"]/text()', 'l'),
                      ('问题补充', '*//div[@class="bpannel"]//div[@class="p20"]/p[@class="mt20"]/p/text()', 'l'),
                      ]

    str_t = []
    for i in range(0, len(question_colum)):
        str_t.append(question_colum[i][0])
    str_t.append("数据来源")
    csv.write_csv_file_line(file_path=path + "/question.csv", str=str_t)

    # 回答结构
    aswer_column=[('获赞数','./div[@class="qa-aswer-content"]/div[@class="qa-aswer-l"]//p/text()','l'),
                  ('留言者','./div[@class="qa-aswer-content"]/div[@class="qa-aswer-r"]/span[1]//text()','l'),
                  ('留言者主页','./div[@class="qa-aswer-content"]/div[@class="qa-aswer-r"]/span/a[@rel="username"]/@href','sab','https://www.xinshipu.com'),
                  ('留言时间','./div[@class="qa-aswer-content"]/div[@class="qa-aswer-r"]/span[@class="cg2 ml22 font12"]/text()','l'),
                  ('留言内容','./div[@class="qa-aswer-content"]/div[@class="qa-aswer-r"]/p[@class="cg1"]/span[1]//text()','l'),
                  ('id', './div[@class="qa-aswer-content"]/div[@class="qa-aswer-l"]//p/@id', 'sp','_',2),
                  ('回复', './div[@class="qa-answer-reply mt17 pr qa-aswer-r "]/div[@class="reply-li"]//text()','sarr')]
    str_t = []
    for i in range(0, len(aswer_column)):
        str_t.append(aswer_column[i][0])
    str_t.append("数据来源")
    csv.write_csv_file_line(file_path=path + "/aswer.csv", str=str_t)

    read_detial(start_url,path,question_colum,aswer_column)


if __name__ == '__main__': # 判断文件入口
    main()
