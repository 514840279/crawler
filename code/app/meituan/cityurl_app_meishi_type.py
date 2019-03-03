#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.HtmlSource import HtmlSource
from common.Rule import Rule
from common.inc_conn import Conn_mysql
from common.inc_file import File_file,File_floder
from common.inc_csv import  Csv_base
import time
import uuid
from lxml import html

htmlSource = HtmlSource()
rule = Rule()
meituan_mysql = Conn_mysql( host='localhost', user='root', passwd='514840279@qq.com', db='app', port=3306,) # 生成MYSQL数据库索引数据实例



# 多页
def main():
    sql ="""
    SELECT * FROM `meituan_city_url`
        WHERE ci_name = '美食'
        AND state<100
        ORDER BY city ASC
    """
    res,data = meituan_mysql.read_sql(sql)
    dropdown = [('leimu', '//div[@class="dropdown-list hook"]/a', 'l'),
                ('addr', '//div[@class="biz-wrapper"]/div/a', 'l')]



    for row in data:
        url = row['ci']
        #print(row)
        html_source = htmlSource.get_html(url_p=url,type_p='rg')
        #print(html_source)
        datat = rule.html_content_analysis_detial(html_text=html_source, column=dropdown, url=url)
        #print(datat)
        if(len(datat[0][1])!=0):
            for row_a in datat[0][1]:
                #print(html.tostring(row_a))
                leimu_dropdown =[('name', './span[1]/text()', 'l'),('num', './span[2]/text()', 'l')]
                leimu_datas =rule._analysis_(tree=row_a, column=leimu_dropdown, url=url)
                if len(leimu_datas[1][1]) == 0:
                    num = 0
                else:
                    num = leimu_datas[1][1][0]
                # 补充更新数据
                if(leimu_datas[0][1][0]=='全部美食'):
                    upd_sql = "update meituan_city_url  set max_size = '%d' where uuid='%d'"%(num,row['uuid'])
                    meituan_mysql.write_sql(upd_sql)
                # 全部类目 插入
                insert_sql = "insert into  meituan_meishi_type values('%s','%s','%s','%s','%s')" %(uuid.uuid4(),row['uuid'],leimu_datas[0][1][0],num,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                print(insert_sql)
                meituan_mysql.write_sql(insert_sql)

if __name__ == '__main__': # 判断文件入口
    main()
