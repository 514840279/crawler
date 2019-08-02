#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from common.RuleConf import Rule
import pymysql
from common.Mysql_Utils import MyPymysqlPool


class PageDict():
    db_pool = MyPymysqlPool("default")
    def runDict(self,url,conf):

        rule = Rule()
        result,nextPage =rule.crawler_list(url,conf)
        print(nextPage)
        # 数据入库 TODO
        dic_list=[]
        for row in conf['columns']:
            dic_list.append(row['名称'])
        self.insertList(result=result,table=conf['tablename'],column_names=dic_list)
        if nextPage is not None and url != nextPage:
            self.runDict(url=nextPage,conf=conf)

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
                    createsql = """create table """ + table + """ (`采集时间` varchar(20),`主键` varchar(32) primary key)"""
                    print(createsql)
                    self.db_pool.update(createsql)
                    for column_name in column_names:
                        altersql = " alter table " + table + " add column `" + column_name + "` varchar(255);"
                        try:
                            self.db_pool.update(altersql)
                        except Exception as e:
                            if e.args[0] == 1060:
                                print(table,column_name,"字段已经存在！")
                            else:
                                print(e.args,"更新表字段")
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
                        updatesql += "`" + column_name + "` = '" + str(row[column_name]).replace("\'", "’").replace(
                            "\\", "") + "'"
                        index += 1
                    updatesql += " where `主键` = '" + row['主键'] + "'"
                    print(updatesql)
                    self.db_pool.update(updatesql)
                    self.db_pool._conn.commit();
                    print("主键重复", pye.args[1])
                else:
                    pye.with_traceback()
            except Exception as e:
                e.with_traceback()




# 测试字典采集
def runDict():
    pageDict = PageDict()
    start_url="http://www.xuexiku.com.cn/html/shenghuo/liyixingxiang/index.html"
    conf={
        "group":'*//div[@class="navbox"]/div[@class="nav"]/table/tbody/tr/td/div//a',
        "tablename": 'xuexiku_dict',
        "columns":[
            {"名称": "主键", "规则": "md5", "类型": "主键","连接": "地址"},
            {"名称": "网站", "规则": "学习库", "类型": "不解析"},
            {"名称": "类别", "规则": ".//text()", "类型": "文本"},
            {"名称": "地址", "规则": "./@href", "类型": "连接"},
            {"名称": "采集时间", "规则": "%Y.%m.%d %H:%M:%S", "类型": "采集时间"},
        ],
    }
    pageDict.runDict(url=start_url,conf=conf)

# 测试字典采集
def pdfrunDict():
    pageDict = PageDict()
    start_url="http://www.anysafer.com/jisuanji/"
    conf={
        "group":'*//div[@class="contentLayout"]//a',
        "tablename": 'pdf电子书下载_dict',
        "columns":[
            {"名称": "主键", "规则": "md5", "类型": "主键","连接": "地址"},
            {"名称": "网站", "规则": "pdf电子书下载", "类型": "不解析"},
            {"名称": "类别", "规则": ".//text()", "类型": "文本"},
            {"名称": "地址", "规则": "./@href", "类型": "连接"},
            {"名称": "采集时间", "规则": "%Y.%m.%d %H:%M:%S", "类型": "采集时间"},
        ],
    }
    pageDict.runDict(url=start_url,conf=conf)


# 测试字典采集
def runWanhe():
    pageDict = PageDict()
    start_url="http://www.hejizhan.com/bbs/?page=1017"
    conf={
        "group":'*//ul[@class="forum-list forum-topic-list"]/li',
        "tablename": '万千合集站_list',
        "columns":[
            {"名称": "主键", "规则": "md5", "类型": "主键","连接": "地址"},
            {"名称": "网站", "规则": "万千合集站", "类型": "不解析"},
            {"名称": "头像", "规则": './div[@class="media"]/a/img/@src', "类型": "图片"},
            {"名称": "个人主页", "规则": './div[@class="media"]/a/@href', "类型": "连接"},
            {"名称": "地址", "规则": './div[@class="info-container"]/div/p/a/@href', "类型": "连接"},
            {"名称": "资料名称", "规则": './div[@class="info-container"]/div/p[@class="title"]/a/text()', "类型": "文本"},
            {"名称": "标签", "规则": './div[@class="info-container"]/div/p[@class="title"]/span[1]/text()', "类型": "文本"},
            {"名称": "分享人", "规则": './div[@class="info-container"]/div/ul[@class="info-start-end"]/li/a[1]/text()', "类型": "文本"},
            {"名称": "分享时间", "规则": './div[@class="info-container"]/div/ul[@class="info-start-end"]/li/text()',"类型": "文本"},
            {"名称": "分类", "规则": './div[@class="info-container"]/div/ul[@class="info-start-end"]/li/a[2]/text()',
             "类型": "文本"},
            {"名称": "采集时间", "规则": "%Y.%m.%d %H:%M:%S", "类型": "采集时间"},
        ],
        "nextPage":'*//ul[@class="pagination"]//li/a[contains(text(),"»")]/@href'
    }
    pageDict.runDict(url=start_url,conf=conf)

if __name__ == '__main__':
    #runDict()
    #pdfrunDict()
    runWanhe()

