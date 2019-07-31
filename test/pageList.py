#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from common.RuleConf import Rule
from common.Mysql_Utils import MyPymysqlPool
import pymysql
import threading, time


class PageList():
    db_pool = MyPymysqlPool("default")

    def __init__(self, confs):
        self.confs = confs

    def runList(self):
        # 数据读取
        # dict = self.readOne(db_pool=self.db_pool, table='xuexi111_dict')
        dictList = self.readAll(db_pool=self.db_pool, table='xuexi111_dict')
        if dictList  is not False:
            # 数据写入
            for dict in dictList:
                self.updateStatue2(db_pool=self.db_pool, table='xuexi111_dict', uuid=dict['uuid'], statue=2)
                for conf in self.confs:
                    url = dict['地址']
                    if dict['current_url'] is not None:
                        url = dict['current_url']
                    self.crawlerNext(conf, url=url, uuid=dict['uuid'])

    def crawlerNext(self, conf, url='', uuid=''):
        print(url, uuid)
        rule = Rule()
        list_list = []
        for row in conf['columns']:
            list_list.append(row['名称'])
        try:
            result, next_page = rule.crawler_list(url, conf)
            if len(result) > 0:

                self.insertList(result=result, table='xuexi111_list', column_names=list_list)
                if next_page:

                    self.updateCurrent(db_pool=self.db_pool, table='xuexi111_dict', uuid=uuid, current=next_page)
                    self.db_pool._conn.commit();
                    self.crawlerNext(conf, url=next_page, uuid=uuid)
                else:

                    self.updateStatue(db_pool=self.db_pool, table='xuexi111_dict', uuid=uuid, statue=1)
                    self.db_pool._conn.commit();
        except Exception as e:
            if '网页访问失败，无内容！' == e.args[0]:
                self.updateStatue2(db_pool=self.db_pool, table='xuexi111_dict', uuid=uuid, statue=-1)
                self.db_pool._conn.commit();



    def readOne(self, db_pool, table=''):
        sql = """ select * from %s where statue  is null or statue =0 for update  """ % table
        return db_pool.getOne(sql)

    def readAll(self, db_pool, table=''):
        sql = """ select * from %s where statue  is null or statue =0 for update  """ % table
        return db_pool.getAll(sql)

    def updateStatue(self, db_pool, table='', uuid='', statue=1):
        sql = """ update %s set statue = %d,current_url=null where uuid='%s' """ % (table, statue, uuid)
        return db_pool.update(sql)

    def updateStatue2(self, db_pool, table='', uuid='', statue=2):
        sql = """ update %s set statue = %d where uuid='%s' """ % (table, statue, uuid)
        return db_pool.update(sql)

    def updateCurrent(self, db_pool, table='', uuid='', current=''):
        sql = """ update %s set current_url='%s' where uuid='%s' """ % (table, current, uuid)
        return db_pool.update(sql)

    def insertList(self, result='', table='', column_names=[]):
        columns = ''
        index = 0
        for column_name in column_names:
            if index > 0:
                columns += ","
            columns += '`' + column_name + '`'
            index += 1


        for row in result:
            index = 0
            values = ''
            for column_name in column_names:
                if index > 0:
                    values += ","
                values += "'" + row[column_name].replace("\'", "’").replace("\\", "") + "'"
                index += 1

            sql = "insert into " + table + " (" + columns + ") values(" + values + ")"
            print(sql)
            try:
                self.db_pool.insert(sql=sql)
                self.db_pool._conn.commit();
            except pymysql.err.ProgrammingError as pye:
                if 1146 == pye.args[0]:
                    createsql = """create table """ + table + """ (`网站` varchar(100),`资料名称` varchar(200),`地址` varchar(2000),`图片` varchar(2000),`jieshao` varchar(2000),`jieshao_low` varchar(2000),`采集时间` varchar(20),`主键` varchar(32) primary key)"""
                    print(createsql)
                    self.db_pool.update(createsql)
                    self.db_pool.insert(sql)
                else:
                    pye.with_traceback()
            except pymysql.err.IntegrityError as pye:
                if 1062 == pye.args[0]:
                    updatesql = "update " + table + " set "
                    index = 0
                    for column_name in column_names:
                        if index > 0:
                            updatesql += ","
                        updatesql += "`" + column_name + "` = '" + row[column_name].replace("\'", "’").replace("\\", "") + "'"
                        index+=1
                    updatesql += " where `主键` = '" + row['主键'] + "'"
                    print(updatesql)
                    self.db_pool.update(updatesql)
                    self.db_pool._conn.commit();
                    print("主键重复", pye.args[1])
                else:
                    pye.with_traceback()
            except Exception as e:
                e.with_traceback()


def runList():
    confs = [{
        "urlname": '地址',
        "group": '*//table[@class="list"]//tr',
        "columns": [
            {"名称": "主键", "规则": "md5", "类型": "主键", "连接": "地址"},
            {"名称": "网站", "规则": "学习资料库", "类型": "不解析"},
            {"名称": "资料名称", "规则": "./td[1]/a/text()", "类型": "文本"},
            {"名称": "地址", "规则": "./td[1]/a/@href", "类型": "连接"},
            {"名称": "资料大小", "规则": "./td[2]/text()", "类型": "文本"},
            {"名称": "资料语言", "规则": "./td[3]/text()", "类型": "文本"},
            {"名称": "采集时间", "规则": "%Y.%m.%d %H:%M:%S", "类型": "采集时间"},
        ],
        "nextPage": '*//div[@class="show-page"]/a[@class="next"]/@href'
    }, {
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
    updateAllStatue(table='xuexi111_dict', statue=2)
    #for i in range(0,12):
    pageDict = PageList(confs)


    pageDict.runList()
    #th = threading.Thread(target=pageDict.runList)
    #th.start()  # 启动线程
    time.sleep(1)
    # pageDict.runList(confs=confs)


def updateAllStatue(table='', statue=2):
    db_pool = MyPymysqlPool("default")
    sql = """ update %s set statue = null where statue = %d """ % (table, statue)
    db_pool.update(sql)
    db_pool.dispose()


if __name__ == '__main__':
    runList()
