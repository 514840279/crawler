#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from common.RuleConf import Rule
from common.Mysql_Utils import MyPymysqlPool
import  pymysql

class PageList():


    def runList(self,confs,dictconf):

        # 数据读取
        db_pool = MyPymysqlPool("default")
        dictList  = self.readList(db_pool=db_pool,table='xuexi111_dict')
        db_pool.dispose()
        # 数据写入
        for dict in dictList:
            for conf in confs:
                self.crawlerNext(conf,url=dict['地址'],uuid=dict['uuid'])

    def crawlerNext(self,conf,url= '',uuid=''):
        print(url,uuid)
        rule = Rule()
        list_list = []
        for row in conf['columns']:
            list_list.append(row['名称'])
        result,next_page = rule.crawler_list(url, conf)
        if(len(result)>0):

            self.insertList(result=result,table='xuexi111_list')
            if(next_page):
                self.crawlerNext(conf,url=next_page,uuid=uuid)
            else:
                db_pool = MyPymysqlPool("default")
                self.updateStatue(db_pool=db_pool,table='xuexi111_dict',uuid=uuid,statue=1)
                db_pool.dispose()
    def readList(self,db_pool,table=''):
        sql =""" select * from %s where statue  is null or statue =0 """ % table
        return db_pool.getAll(sql)

    def updateStatue(self,db_pool,table='',uuid='',statue=1):
        sql = """ update %s set statue = %d where uuid='%s' """ % (table,statue,uuid)
        return db_pool.update(sql)

    def insertList(self,result='',table=''):
        db_pool = MyPymysqlPool("default")
        sql="insert into "+table+" (`网站`,`资料名称`,`地址`,`图片`,`jieshao`,`jieshao_low`,`采集时间`,`主键`) values('%s','%s','%s','%s','%s','%s','%s','%s')"
        for row in result:
            params = (row['网站']
                      ,row['资料名称'].replace("\\","").replace("'","\\\'")
                      ,row['地址']
                      ,row['图片']
                      ,row['jieshao'].replace("\\","").replace("'","\\\'")
                      ,row['jieshao_low'].replace("\\","").replace("'","\\\'")
                      ,row['采集时间']
                      ,row['主键']
                      )
            print(sql % params)
            try:
                db_pool.insert(sql=sql % params)

            except pymysql.err.ProgrammingError as pye:
                if(1146 == pye.args[0]):
                    createsql = """create table """+table+""" (`网站` varchar(100),`资料名称` varchar(200),`地址` varchar(2000),`图片` varchar(2000),`jieshao` varchar(2000),`jieshao_low` varchar(2000),`采集时间` varchar(20),`主键` varchar(32) primary key)"""
                    print(createsql)
                    db_pool.update(createsql)
                    db_pool.insert(sql,param=params)
                else:
                    pye.with_traceback()
            except pymysql.err.IntegrityError as pye:
                if (1062 == pye.args[0]):
                    print("主键重复", pye.args[1])
                else:
                    pye.with_traceback()
            except Exception as e:
                e.with_traceback()
        db_pool.dispose()
def runList():

    pageDict = PageList()
    dictconf = {
        "group": '*//div[@class="site-map"]/a',
        "columns": [
            {"名称": "主键", "规则": "md5", "类型": "主键", "连接": "地址"},
            {"名称": "网站", "规则": "学习资料库", "类型": "不解析"},
            {"名称": "类别", "规则": ".//text()", "类型": "文本"},
            {"名称": "地址", "规则": "./@href", "类型": "连接"},
            {"名称": "采集时间", "规则": "%Y.%m.%d %H:%M:%S", "类型": "采集时间"},
        ],
    }
    confs = [{
        "urlname": '地址',
        "group": '*//table[@class="list"]//tr',
        "columns": [
            {"名称": "主键", "规则": "md5", "类型": "主键", "连接": "地址"},
            {"名称": "网站", "规则": "学习资料库", "类型": "不解析"},
            {"名称": "资料名称", "规则": "./td[1]/a/text()", "类型": "文本"},
            {"名称": "地址", "规则": "./td[1]/a/@href", "类型": "连接"},
            {"名称": "资料大小", "规则": "./td[2]/text()", "类型": "连接"},
            {"名称": "资料语言", "规则": "./td[3]/text()", "类型": "连接"},
            {"名称": "采集时间", "规则": "%Y.%m.%d %H:%M:%S", "类型": "采集时间"},
        ],
        "nextPage":'*//div[@class="show-page"]/a[@class="next"]/@href'
    },{
        "urlname": '地址',
        "group": '*//div[@class="topic-list"]/ul/li',
        "columns": [
            {"名称": "主键", "规则": "md5", "类型": "主键", "连接": "地址"},
            {"名称": "网站", "规则": "学习资料库", "类型": "不解析"},
            {"名称": "资料名称", "规则": "./h3/a/text()", "类型": "文本"},
            {"名称": "地址", "规则": "./h3/a/@href", "类型": "连接"},
            {"名称": "图片", "规则": './a/img/@src', "类型": "图片"},
            {"名称": "jieshao", "规则": './div[@class="jieshao"]//text()', "类型": "文本"},
            {"名称": "jieshao_low", "规则": './div[@class="jieshao-low"]//text()', "类型": "文本"},
            {"名称": "采集时间", "规则": "%Y.%m.%d %H:%M:%S", "类型": "采集时间"},
        ],
        "nextPage": '*//div[@class="show-page"]/a[@class="next"]/@href'
    }]
    pageDict.runList(confs=confs,dictconf=dictconf)




if __name__ == '__main__':
    runList()

