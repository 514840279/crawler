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

#-----系统外部需安装库模块引用-----

#-----DIY自定义库模块引用-----

#--------- 外部模块处理<<结束>> ---------#

#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

# ---全局变量处理

# ---本模块内部类或函数定义区
def run_it():
    
    res_list = {} #抽取结果字典
    #标准测试文件
    with open("../data/temp.html") as f:
        html_code = f.read()
        #print(html_code)
    
    # 结构化爬虫测试
    name_model = "z_code_0"
    run_model =__import__(name_model)
    
    #输入量 html_code,网页源码 todo 推荐处理方式 lx:lxml bs:BeautifulSoup re:regular
    res_list = run_model.run_it(html_code,to_do="lx",url="http://jobs.51job.com/hangzhou-xcq/91103248.html?s=04")
    
    print (res_list)

    #5 视任务的特性 决定是否删除 临时代码文件 temp_方法ID.py
    

    
#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#

def main():
    import shutil
    #1 过程一
    run_it()
    #2 过程二
    #3 过程三
    
if __name__ == '__main__':
    main()
    
#---------- 主过程<<结束>> -----------#