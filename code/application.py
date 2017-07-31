#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----

import sys # 操作系统模块1
import os # 操作系统模块2
import types # 数据类型
import time # 时间模块
import datetime # 日期模块
#-----DIY自定义库模块引用-----

# ---全局变量处理

# ---本模块内部类或函数定义区
def run_it():



    # 结构化爬虫测试
    name_model = "z_code_0"
    run_model =__import__(name_model)
    run_model.run_it(html="1",url="fs")

    
#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#

def main():
    run_it()

    
if __name__ == '__main__':
    main()
    
#---------- 主过程<<结束>> -----------#