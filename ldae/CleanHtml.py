#!/usr/bin/env python
# coding=utf-8

from common.inc_csv import Csv_base
from lxml import html
import re

def readFile(filePath=''):
    pass


if __name__ == '__main__':
    filepath='../data/问答语料_1.0.txt'
    file = Csv_base()
    list = file.read_csv_file(filepath)
    for i in range(len(list)):
        if(i>3):
            row = list[i]
            rows= str(row[0]).split("\t")
            html_text = rows[1].replace("[",'').replace("]","")
            # 正则匹配 re.match从字符串起始处匹配。
            html_text = re.sub(re.compile(r"<script.*?</script>", re.S), "", html_text)

            print(html_text)
            tree = html.fromstring(html_text)
            texts = tree.xpath('.//text()')
            text=""
            for a in texts:
                text=text+str(a).replace("\\n",".").strip()
            row_content = [rows[0],text]
            file.write_csv_file_line(file_path="../data/问答语料_1.0.csv",str=row_content)