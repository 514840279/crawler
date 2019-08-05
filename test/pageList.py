#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from common.RuleConf import Rule
from common.Mysql_Utils import MyPymysqlPool
import pymysql
import threading, time


class PageList():
    db_pool = MyPymysqlPool("default")

    def runList(self,confs):
        dictable = confs[0]['urltable']
        print(dictable)
        #self.updateAllStatue(table=dictable, statue=2)
        # 数据读取
        # dict = self.readOne(db_pool=self.db_pool, table='xuexi111_dict')
        try:
            self.updateAllStatue(table=confs[0]['urltable'], statue=2)
            dictList = self.readAll(db_pool=self.db_pool, table=dictable)
            if dictList  is not False:
                # 数据写入
                for dict in dictList:
                    self.updateStatue2(db_pool=self.db_pool, table=dictable, uuid=dict['主键'], statue=2)
                    for conf in confs:
                        url = dict[conf['urlname']]
                        if dict['current_url'] is not None:
                            url = dict['current_url']
                        type_p='rg'
                        if 'readtype' in conf.keys():
                            type_p = conf['readtype']
                        self.crawlerNext(conf, url=url, uuid=dict['主键'],type_p=type_p)
        except Exception as e:
            print(e.args,"runList")
            if(e.args[0] == 1054):
                try:
                    altersql = " alter table `" + dictable + "` add column `statue` int(2)"
                    self.db_pool.update(altersql)
                except Exception as e:
                    if e.args[0] == 1060:
                        print(dictable,  " statue 字段已经存在！")
                    else:
                        print(e.args, "更新表字段")
                try:
                    altersql = " alter table `" + dictable + "` add column `更新时间` timestamp on update current_timestamp"
                    self.db_pool.update(altersql)
                except Exception as e:
                    if e.args[0] == 1060:
                        print(dictable,  "更新时间 字段已经存在！")
                    else:
                        print(e.args, "更新表字段")
                try:
                    altersql = " alter table `" + dictable + "` add column `current_url` varchar(500)"
                    self.db_pool.update(altersql)
                except Exception as e:
                    if e.args[0] == 1060:
                        print(dictable,  "current_url 字段已经存在！")
                    else:
                        print(e.args, "更新表字段")
            if(e.args[0] == "更新时间"):
                try:
                    altersql = " alter table `" + dictable + "` add column `更新时间` timestamp on update current_timestamp"
                    self.db_pool.update(altersql)
                except Exception as e:
                    if e.args[0] == 1060:
                        print(dictable,  "更新时间 字段已经存在！")
                    else:
                        print(e.args, "更新表字段")
            if('current_url' == e.args[0] ):
                try:
                    altersql = " alter table `" + dictable + "` add column `current_url` varchar(500)"
                    self.db_pool.update(altersql)
                except Exception as e:
                    if e.args[0] == 1060:
                        print(dictable,  "current_url 字段已经存在！")
                    else:
                        print(e.args, "更新表字段")
            self.runList(confs)
    def crawlerNext(self, conf, url='', uuid='',type_p='rg'):
        print(url, uuid)
        try:
            rule = Rule()
            result, next_page = rule.crawler_list(url, conf,type_p=type_p)
            print(next_page)
            if len(result) > 0:
                list_list = []
                for row in conf['columns']:
                    list_list.append(row['名称'])
                self.insertList(result=result, table=conf['tablename'], column_names=list_list)
                if next_page is not None and url != next_page:
                    self.updateCurrent(db_pool=self.db_pool, table=conf['urltable'], uuid=uuid, current=next_page)
                    self.db_pool._conn.commit();
                    self.crawlerNext(conf, url=next_page, uuid=uuid,type_p=type_p)
                else:
                    self.updateStatue(db_pool=self.db_pool, table=conf['urltable'], uuid=uuid, statue=1)
                    self.db_pool._conn.commit();
        except Exception as e:
            print(e.args,'crawlerNext')
            if 1001 == e.args[0]:
                self.updateStatue2(db_pool=self.db_pool, table=conf['urltable'], uuid=uuid, statue=-1)
                self.db_pool._conn.commit();
            if e.args[0] == 1054:
                try:
                    altersql = " alter table `" + conf['urltable'] + "` add column `更新时间` timestamp on update current_timestamp"
                    self.db_pool.update(altersql)
                except Exception as e:
                    if e.args[0] == 1060:
                        print(conf['urltable'], "更新时间 字段已经存在！")
                    else:
                        print(e.args, "更新表字段")
                try:
                    altersql = " alter table `" + conf['urltable'] + "` add column `current_url` varchar(500)"
                    self.db_pool.update(altersql)
                except Exception as e:
                    if e.args[0] == 1060:
                        print(conf['urltable'], "current_url 字段已经存在！")
                    else:
                        print(e.args, "更新表字段")
                self.crawlerNext(conf, url, uuid)


    def readOne(self, db_pool, table=''):
        sql = """ select * from %s where statue  is null or statue =0 for update  """ % table
        return db_pool.getOne(sql)

    def readAll(self, db_pool, table=''):
        sql = """ select * from %s where statue  is null or statue =0  """ % table
        return db_pool.getAll(sql)

    def updateStatue(self, db_pool, table='', uuid='', statue=1):
        sql = """ update %s set statue = %d,current_url=null where 主键='%s' """ % (table, statue, uuid)
        return db_pool.update(sql)

    def updateAllStatue(self,table='', statue=2):
        db_pool = MyPymysqlPool("default")
        sql = """ update %s set statue = null where statue = %d """ % (table, statue)
        db_pool.update(sql)
        db_pool.dispose()

    def updateStatue2(self, db_pool, table='', uuid='', statue=2):
        sql = """ update %s set statue = %d where 主键='%s' """ % (table, statue, uuid)
        return db_pool.update(sql)

    def updateCurrent(self, db_pool, table='', uuid='', current=''):
        sql = """ update %s set current_url='%s' where 主键='%s' """ % (table, current, uuid)
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
                values += "'" + str(row[column_name]).replace("\'", "’").replace("\\", "") + "'"
                index += 1

            sql = "insert into `" + table + "` (" + columns + ") values(" + values + ")"
            print(sql)
            try:
                self.db_pool.insert(sql=sql)
                self.db_pool._conn.commit();
            except pymysql.err.ProgrammingError as pye:
                if 1146 == pye.args[0]:
                    createsql = """create table `""" + table + """` (`采集时间` varchar(20),`主键` varchar(32) primary key)  DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci"""
                    print(createsql)
                    self.db_pool.update(createsql)
                    for column_name in column_names:
                        altersql = " alter table `"+table +"` add column `"+column_name+"` varchar(255);"
                        try:
                            self.db_pool.update(altersql)
                        except Exception as e:
                            if e.args[0] == 1060:
                                print(table, column_name, "字段已经存在！")
                            else:
                                print(e.args, "更新表字段")
                    self.db_pool.insert(sql)
                    self.db_pool._conn.commit();
                else:
                    pye.with_traceback()
            except pymysql.err.IntegrityError as pye:
                if 1062 == pye.args[0]:
                    updatesql = "update " + table + " set "
                    index = 0
                    for column_name in column_names:
                        if index > 0:
                            updatesql += ","
                        updatesql += "`" + column_name + "` = '" + str(row[column_name]).replace("\'", "’").replace("\\", "") + "'"
                        index+=1
                    updatesql += " where `主键` = '" + row['主键'] + "'"
                    print(updatesql)
                    self.db_pool.update(updatesql)
                    self.db_pool._conn.commit();
                    print("主键重复", pye.args[1])
                else:
                    pye.with_traceback()
            except Exception as e:
                print(e.args,"insertList")
                if e.args[0] == 1406:
                    column = e.args[1]
                    column = column[column.index("'")+1:column.rindex("'")]
                    altersql = "alter table "+table+" modify column "+column+" varchar(2000)"
                    self.db_pool.update(sql=altersql)
                    self.insertList(result,table,column_names)



def runList():
    confs = [{
        "urltable":"xuexi111_dict",
        "urlname": '地址',
        "tablename":"xuexi111_list",
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
        "urltable":"xuexi111_dict",
        "urlname": '地址',
        "tablename":"xuexi111_list",
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

    #for i in range(0,12):
    pageDict = PageList()
    pageDict.updateAllStatue(table="xuexi111_dict", statue=2)
    pageDict.runList(confs)
    #th = threading.Thread(target=pageDict.runList)
    #th.start()  # 启动线程
    time.sleep(1)
    # pageDict.runList(confs=confs)


def runListXuexiku():
    confs = [{
        "urltable":"xuexiku_dict",
        "urlname": '地址',
        "tablename":"xuexiku_list",
        "group": '*//ul[@class="mlist"]//li',
        "columns": [
            {"名称": "主键", "规则": "md5", "类型": "主键", "连接": "地址"},
            {"名称": "网站", "规则": "学习库", "类型": "不解析"},
            {"名称": "图片", "规则": './a/img/@src', "类型": "图片"},
            {"名称": "资料名称", "规则": './div[@class="info"]/h2/a/text()', "类型": "文本"},
            {"名称": "地址", "规则": './div[@class="info"]/h2/a/@href', "类型": "连接"},
            {"名称": "类别", "规则": './div[@class="info"]/p[1]/text()', "类型": "文本"},
            {"名称": "语言", "规则": './div[@class="info"]/p[2]/i/text()', "类型": "文本"},
            {"名称": "大小", "规则": './div[@class="info"]/p[3]/i/text()', "类型": "文本"},
            {"名称": "浏览", "规则": './div[@class="info"]/p[4]/i[1]/text()', "类型": "文本"},
            {"名称": "更新", "规则": './div[@class="info"]/p[4]/i[2]/text()', "类型": "文本"},
            {"名称": "采集时间", "规则": "%Y.%m.%d %H:%M:%S", "类型": "采集时间"},
        ],
        "nextPage": '*//div[@class="pagelist1"]/a[@class="thispage"]/following-sibling::a[1]/@href'
    }]

    #for i in range(0,12):
    pageDict = PageList()
    pageDict.updateAllStatue(table=confs[0]['urltable'], statue=2)
    pageDict.runList(confs)
    #th = threading.Thread(target=pageDict.runList)
    #th.start()  # 启动线程
    time.sleep(1)
    # pageDict.runList(confs=confs)


def runListPdf():
    confs = [{
        "urltable":"pdf电子书下载_dict",
        "urlname": '地址',
        "tablename":"pdf电子书下载_list",
        "group": '*//div[@class="rightBlock"]/div[@class="bookinfo"]',
        "columns": [
            {"名称": "主键", "规则": "md5", "类型": "主键", "连接": "地址"},
            {"名称": "网站", "规则": "pdf电子书下载", "类型": "不解析"},
            {"名称": "资料名称", "规则": './h2/a/text()', "类型": "文本"},
            {"名称": "地址", "规则": './h2/a/@href', "类型": "连接"},
            {"名称": "星", "规则": './h2/span/img/@src', "类型": "图片"},
            {"名称": "简介", "规则": './div[@class="bookdesc"]//text()', "类型": "文本"},
            {"名称": "关键字", "规则": './div[@class="booktags"]/a//text()', "类型": "数组"},
            {"名称": "类别", "规则": './div[@class="bookmore"]/span[1]/text()', "类型": "文本"},
            {"名称": "格式", "规则": './div[@class="bookmore"]/span[2]/text()', "类型": "文本"},
            {"名称": "下载", "规则": './div[@class="bookmore"]/span[3]/text()', "类型": "文本"},
            {"名称": "大小", "规则": './div[@class="bookmore"]/span[4]/text()', "类型": "文本"},
            {"名称": "时间", "规则": './div[@class="bookmore"]/span[5]/text()', "类型": "文本"},
            {"名称": "采集时间", "规则": "%Y.%m.%d %H:%M:%S", "类型": "采集时间"},
        ],
        "nextPage": '*//div[@class="pageBar"]/a[contains(text(),"下一页")]/@href'
    }]
    pageDict = PageList()
    pageDict.runList(confs)

def runListPdf():
    confs = [{
        "urltable":"xiaoshuo530_dict",
        "urlname": '地址',
        "tablename":"xiaoshuo530_list",
        "group": '*//div[@class="l"]/ul/li]',
        "columns": [
            {"名称": "主键", "规则": "md5", "类型": "主键", "连接": "地址"},
            {"名称": "网站", "规则": "xiaoshuo530", "类型": "不解析"},
            {"名称": "资料名称", "规则": './span[@class="s2"]/a/text()', "类型": "文本"},
            {"名称": "地址", "规则": './span[@class="s2"]/a/@href', "类型": "连接"},
            {"名称": "标签", "规则": './span[@class="s1"]/text()', "类型": "文本"},
            {"名称": "最新章节", "规则": './span[@class="s3"]/a/text()', "类型": "文本"},
            {"名称": "章节地址", "规则": './span[@class="s3"]/a/@href', "类型": "连接"},
            {"名称": "作者", "规则": './span[@class="s4"]/a/text()', "类型": "文本"},
            {"名称": "作者地址", "规则": './span[@class="s4"]/a/@href', "类型": "连接"},
            {"名称": "文章更新时间", "规则": './span[@class="s5"]/a/@href', "类型": "文本"},
            {"名称": "采集时间", "规则": "%Y.%m.%d %H:%M:%S", "类型": "采集时间"},
        ],
        "nextPage": '*//div[@class="pageBar"]/a[contains(text(),"下一页")]/@href'
    }]
    pageDict = PageList()
    pageDict.runList(confs)

def runxxbqg5200():
    confs = [{
        "urltable": "xxbqg5200_dict",
        "urlname": '地址',
        "tablename": "xxbqg5200_list",
        "group": '*//div[@class="l"]/ul/li',
        "columns": [
            {"名称": "主键", "规则": "md5", "类型": "主键", "连接": "地址"},
            {"名称": "网站", "规则": "xxbqg5200", "类型": "不解析"},
            {"名称": "资料名称", "规则": './span[@class="s2"]/a/text()', "类型": "文本"},
            {"名称": "地址", "规则": './span[@class="s2"]/a/@href', "类型": "连接"},
            {"名称": "标签", "规则": './span[@class="s1"]/text()', "类型": "文本"},
            {"名称": "最新章节", "规则": './span[@class="s3"]/a/text()', "类型": "文本"},
            {"名称": "章节地址", "规则": './span[@class="s3"]/a/@href', "类型": "连接"},
            {"名称": "作者", "规则": './span[@class="s4"]/a/text()', "类型": "文本"},
            {"名称": "作者地址", "规则": './span[@class="s4"]/a/@href', "类型": "连接"},
            {"名称": "文章更新时间", "规则": './span[@class="s5"]/a/@href', "类型": "文本"},
            {"名称": "采集时间", "规则": "%Y.%m.%d %H:%M:%S", "类型": "采集时间"},
        ],
        "nextPage": '*//div[@class="page_b"]//a[@class="next"]/@href'
    }]
    pageDict = PageList()
    pageDict.runList(confs)


def runvodxc():
    confs = [{
        "urltable": "星辰影院_dict",
        "urlname": '地址',
        "tablename": "星辰影院_list",
        "group": '*//ul[@class="show-list grid-mode fn-clear"]/li',
        "columns": [
            {"名称": "主键", "规则": "md5", "类型": "主键", "连接": "地址"},
            {"名称": "网站", "规则": "星辰影院", "类型": "不解析"},
            {"名称": "资料名称", "规则": './h5/a/text()', "类型": "文本"},
            {"名称": "地址", "规则": './h5/a/@href', "类型": "连接"},
            {"名称": "演员", "规则": './p[@class="actor"]/a', "类型": "group",'columns':[
                {"名称": "演员名称", "规则": './text()', "类型": "文本"},
                {"名称": "演员地址", "规则": './@href', "类型": "连接"},
            ]},
            {"名称": "图片", "规则": './a/img/@src', "类型": "图片"},
            {"名称": "画质", "规则": './a/em/@id', "类型": "文本"},
            {"名称": "分类1", "规则": './a/div[@class="tagmv"]/em/text()', "类型": "文本"},
            {"名称": "采集时间", "规则": "%Y.%m.%d %H:%M:%S", "类型": "采集时间"},
        ],
        "nextPage": '*//div[@class="pages long-page"]//a[@class="next pagegbk"]/@href'
    }]
    pageDict = PageList()
    pageDict.runList(confs)

def kisssub():
    confs = [{
        "urltable": "爱恋动漫BT下载_dict",
        "urlname": '地址',
        "tablename": "爱恋动漫BT下载_list",
        "group": '*//table[@id="listTable"]/tbody/tr',
        "columns": [
            {"名称": "主键", "规则": "md5", "类型": "主键", "连接": "地址"},
            {"名称": "网站", "规则": "爱恋动漫BT下载", "类型": "不解析"},
            {"名称": "资料名称", "规则": './td[3]/a[1]/text()', "类型": "文本"},
            {"名称": "地址", "规则": './td[3]/a[1]/@href', "类型": "连接"},
            {"名称": "发表时间", "规则": './td[1]/text()', "类型": "文本"},
            {"名称": "类别", "规则": './td[2]//text()', "类型": "文本"},
            {"名称": "大小", "规则": './td[4]//text()', "类型": "文本"},
            {"名称": "种子", "规则": './td[5]//text()', "类型": "文本"},
            {"名称": "下载", "规则": './td[6]//text()', "类型": "文本"},
            {"名称": "完成", "规则": './td[7]//text()', "类型": "文本"},
            {"名称": "UP主_代号", "规则": './td[8]//text()', "类型": "文本"},
            {"名称": "采集时间", "规则": "%Y.%m.%d %H:%M:%S", "类型": "采集时间"},
        ],
        "nextPage": '*//div[@class="pages clear"]//a[contains(text(),"〉")]/@href'
    }]
    pageDict = PageList()
    pageDict.runList(confs)


if __name__ == '__main__':
    #runList()
    #runListXuexiku()
    #runListPdf()
    #runxxbqg5200()
    #runvodxc()
    kisssub()