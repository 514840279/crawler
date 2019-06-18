#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

'''
{
"版权":"LDAE工作室",
"author":{
"1":"集体",
}
"初创时间:"2017年3月",
}
'''

#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----

import sys # 操作系统模块1
import os # 操作系统模块2
import types # 数据类型
import time # 时间模块
import datetime # 日期模块
import pymysql
#-----系统外部需安装库模块引用-----


#-----DIY自定义库模块引用-----
sys.path.append("..")
import csv #CSV组件
import common.inc_sys as inc_sys #自定义基础组件

#--------- 外部模块处理<<结束>> ---------#


#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

# ---全局变量处理


# ---本模块内部类或函数定义区

#继承字符扩展对象
class Csv_base(inc_sys.String_what):


    # CSV 文件读取
    def read_csv_file(self,file_path='../data/test/one.csv'):
        list = []
        #打开文件，用with打开可以不用去特意关闭file了，python3不支持file()打开文件，只能用open()
        with open(file_path,"r",encoding="utf-8") as csvfile:
            #读取csv文件，返回的是迭代类型
            read = csv.reader(csvfile)
            for item in read:
                list.append(item)
        return list

    # CSV 文件读取
    def read_csv_file_line(self,file_path='../data/test/one.csv',line=0):
        #打开文件，用with打开可以不用去特意关闭file了，python3不支持file()打开文件，只能用open()
        csv_list = []
        with open(file_path,"r",encoding="utf-8") as csvfile:
            #读取csv文件，返回的是迭代类型
            read = csv.reader(csvfile)
            for i,rows in enumerate(read):
                
                if (i > line):
                    break
                else:
                    csv_list.append(rows)
                    
        return csv_list

    # CSV 文件写入取
    def write_csv_file_line(self, file_path='',mode='a+',str=[]):
        # 打开文件，追加a
        out = open(file_path,mode=mode, newline='', encoding="utf-8")
        # 设定写入模式
        csv_write = csv.writer(out, dialect='excel')
        # 写入具体内容
        csv_write.writerow(str)

    # CSV 文件写入取
    def write_csv_file_dictLine(self, file_path='',mode='a+',str=[],fieldnames=[]):
        # 打开文件，追加a
        out = open(file_path,mode=mode, newline='', encoding="utf-8")
        # 设定写入模式
        csv_write = csv.DictWriter(out,fieldnames = fieldnames, dialect='excel')
        # 写入具体内容
        csv_write.writerow(str)

#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#

def main():

    print ("") #调试用
    
if __name__ == '__main__':
    
    main()
    
#---------- 主过程<<结束>> -----------#