#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# --------- 外部模块处理<<开始>> ---------#

# -----系统自带必备模块引用-----

import sys  # 操作系统模块1
import os  # 操作系统模块2
import types  # 数据类型
import time  # 时间模块
import datetime  # 日期模块

#-----DIY自定义库模块引用-----
from db.inc_conn import *

# ---全局变量处理

applicationDb = Conn_mysql() # 读取配置信息
resultDb = Conn_mysql(db="result") # 结果入库

# ---本模块内部类或函数定义区
def run_it(*args,**kwargs):
    # 接受要采集的种子信息和地址信息，
    item = url=kwargs['item']
    # 判读有配置模板信息
    uri = item["uuid"]
    list=[]
    # 如果有调用网页采集程序，调用规则提取数据，调用结果配置数据入库，完成采集任务
    if(len(list)>0):
        # 获取网页源码（HtmlSource）
        # 粗提取url
        # 判断url是否当前的网站内地址
        # 如果是入库标记状态0
        # 如果不是丢弃url
        # 将网页源码和当前url传递给（Rule）获得结果
        # 调用ResultData入库
        pass



# --------- 内部模块处理<<结束>> ---------#

# ---------- 主过程<<开始>> -----------#

def main():
    run_it()


if __name__ == '__main__':
    main()

    # ---------- 主过程<<结束>> -----------#