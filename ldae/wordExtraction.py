# -- coding: UTF-8 --

import re


f = open("寒暄语料.txt",encoding='UTF-8')             # 返回一个文件对象
line = f.readline()             # 调用文件的 readline()方法
while line:
    pattern = re.compile(r'.*?([\u4E00-\u9FA5]+)')  # 查找数字
    result1 = pattern.findall(line)
    print(result1)                 # 后面跟 ',' 将忽略换行符
    print(line, ) # 在 Python 3中使用
    line = f.readline()

f.close()