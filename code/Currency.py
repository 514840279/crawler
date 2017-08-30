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
from common.HtmlSource import *
from common.Rule import *
from common.ResultData import *

# ---全局变量处理

applicationDb = Conn_mysql() # 读取配置信息
resultDb = Conn_mysql(db="result") # 结果入库

# ---本模块内部类或函数定义区
def run_it(*args,**kwargs):
    # 接受要采集的种子信息和地址信息，
    uuid =kwargs['uuid']
    url = kwargs['url']
    uri = kwargs['uri']
    # 判读有配置模板信息
    sql = '''
        SELECT  `uuid`,`charset`,`request_type`,`sub_uri`,`type`
        FROM `application`.`sys_seed_ruler_info`
        WHERE delete_flag = 0
        and seed_uuid = '%s'
    ''' % (uuid)
    res ,datarole = applicationDb.read_sql(sql)

    lastrole=()
    urllen = 0
    for i in datarole:
        if url.find(i[3]) > -1:
            if len(i[3]) > urllen:
                lastrole = i
                urllen = len(i[3])
    # 获取网页源码（HtmlSource）
    htmlSource = HtmlSource()
    if len(lastrole) > 0:
        html_text = htmlSource.get_html(url_p=url, type_p=lastrole[2], chartset_p=lastrole[1])
    else:
        html_text = htmlSource.get_html(url_p=url)
    rule = Rule()
    # 粗提取url
    list_a = htmlSource.get_url_list_xpath(html_text)
    list_a = htmlSource.addr_clear(list_a) # 去噪点去重复
    list_a = htmlSource.addr_whole(list_a,url_root= rule.get_url_root(url)) # 补全路径
    # 判断url是否当前的网站内地址 TODO
        # 如果是入库标记状态0
        # 如果不是丢弃url
    # 数据入库
    for a in list_a:
        sql ='''
            INSERT INTO `result`.`sys_url_info`
            VALUES ('%s', '%s',0)
        '''%(rule.get_md5_value(a),a)
        resultDb.write_sql(sql)
    print("网页链接提取完毕.")
    if(len(lastrole) > 0):
        print("读取模板信息.")
        # 获取模板信息
        sql ='''
            SELECT `colum_name`,`ruler`,`type`,`app1`,`app2`,`arr`,`spl1`,`spl2`
            FROM `application`.`sys_seed_ruler_colum_info`
            where delete_flag = 0
            and ruler_uuid = '%s'
        ''' %(lastrole[0])
        res2, columrole = applicationDb.read_sql(sql)

        # 如果有调用网页采集程序，调用规则提取数据，调用结果配置数据入库，完成采集任务
        if(len(columrole)>0):
            print(columrole)
            # 将网页源码和当前url传递给（Rule）获得结果
            result=[]
            if lastrole[4] == 'detial':
                print("详细页面信息提取.")
                result = rule.html_content_analysis_detial(html_text=html_text, column=columrole, url=url)

            elif  lastrole[4] =='list':
                print("列表页面信息提取.")
                result = rule.html_content_analysis_list(html_text=html_text,column=columrole,url=url)

            # 调用ResultData入库
            rd = ResultData()
            rd.resultRefulence(rule_uuid=lastrole[0], result=result,type=lastrole[4] )


    # 更新url
    sql ='''
        UPDATE `result`.`sys_url_info`
        SET `flag` = 2
        WHERE `url` = '%s'
    ''' %(url)
    resultDb.write_sql(sql)
    # 采集完成


# --------- 内部模块处理<<结束>> ---------#

# ---------- 主过程<<开始>> -----------#

def main():
    run_it()


if __name__ == '__main__':
    main()

    # ---------- 主过程<<结束>> -----------#