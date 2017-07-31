#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----

#-----DIY自定义库模块引用-----
from db.inc_conn import *

# ---全局变量处理

applicationDb = Conn_mysql() # 读取配置信息
resultDb = Conn_mysql(db="result") # 结果入库

# ---本模块内部类或函数定义区
def run_it():

    # 读取所有配置信息
    sql = "select * from sys_seed_url_info a"
    res,conf_list = applicationDb.read_sql(sql)

    # 读取网页地址列表
    sql = "select * from sys_url_info where flag = 0 limit 0,100"
    rec,url_list = resultDb.read_sql(sql)

    # 判断每一个地址是否有配置信息
    flag = True
    for item in url_list:
        for list_a in conf_list:
            # 如果有进入采集程序
            if item['url'].find(list_a['seed_url']) > 0:
                flag = False
                # 引入通用模块
                name_model = "Currency"
                run_model =__import__(name_model)
                run_model.run_it(item=item)
        if flag:
            # 如果没有自动添加新的配置信息，并提示用户进行修改 状态修改-1
            sql = "update sys_url_info set flag =-1 where md5='"+item['md5']+"'"
            applicationDb.write_sql(sql)
    
#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#

def main():
    run_it()

if __name__ == '__main__':
    main()
    
#---------- 主过程<<结束>> -----------#