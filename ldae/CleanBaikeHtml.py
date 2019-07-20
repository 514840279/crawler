#!/usr/bin/env python
# coding=utf-8

from common.inc_csv import Csv_base
from common.inc_file import File_file
from lxml import html
import re

csv = Csv_base()
file = File_file()

def replaceStr(a):
    print(a)
    a = re.sub(re.compile(r"收藏查看我的收藏(\d+)有用(.*?)(\d+)已投票(\d+)", re.S), "", a)
    a = str(a).replace("编辑锁定", " ").strip()
    a = str(a).replace("讨论999", " ").strip()
    a = str(a).replace("本词条缺少概述图，补充相关内容使词条更完整，还能快速升级，赶紧来编辑吧！", " ").strip()
    a = str(a).replace("百度百科内容由网友共同编辑，如您发现自己的词条内容不准确或不完善，欢迎使用本人词条编辑服务（免费）参与修正。", " ").strip()
    a = str(a).replace("立即前往 >>", " ").strip()
    print(a)
    return a

if __name__ == '__main__':

    csv_data_path = "../../data/百科候选关键词.csv"
    rows =  csv.read_csv_file(csv_data_path)
    for row in rows:
        try:
            html_data_path=str(row[11]).replace("`","")
            #print("../"+html_data_path)
            html_context = file.open_source2(file_path="../"+html_data_path+".html")

            # 正则匹配 re.match从字符串起始处匹配。
            html_text = re.sub(re.compile(r"<script.*?</script>", re.S), "", html_context)
            tree = html.fromstring(html_text)
            texts = tree.xpath('.//div[@class="main-content"]//text()')
            text = ""
            for a in texts:
                text = text + str(a).replace("\\n", " ").strip()
            text = replaceStr(text)
            #print(text)

            data_str = [html_data_path,text]
            csv.write_csv_file_line(file_path="../data/clean百科候选关键词.csv",str=data_str)
        except FileNotFoundError as notfile:
            csv.write_csv_file_line("../data/nofile.csv",str=row)
        except Exception as e:

            print(e)