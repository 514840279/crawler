#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from common.RuleConf import Rule
from common.inc_csv import Csv_base

class PageDict():

    def runDict(self,url,conf):
        rule = Rule()
        result =rule.crawler_list(url,conf)
        # 数据入库 TODO
        dic_list=[]
        for row in conf['columns']:
            dic_list.append(row['名称'])
        # 文件写入文件
        csv = Csv_base()
        csv.write_csv_file_dictLines(file_path='../data/xuexi111.csv',strs=result,fieldnames=dic_list)

    def runList(self,file_path,confs,dictconf):

        csv = Csv_base()
        # 数据读取
        dic_list = []
        for row in dictconf['columns']:
            dic_list.append(row['名称'])
        dictList = csv.read_csv_file_dict(file_path=file_path,fieldnames=dic_list)

        # 数据写入
        for dict in dictList:
            for conf in confs:
                self.crawlerNext(conf,url=dict[conf['urlname']])


    def crawlerNext(self,conf,url= ''):
        rule = Rule()
        csv = Csv_base()
        list_list = []
        for row in conf['columns']:
            list_list.append(row['名称'])
        result,next_page = rule.crawler_list(url, conf)
        print(result)
        csv.write_csv_file_dictLines(file_path='../data/xuexi111List.csv', strs=result, fieldnames=list_list)
        if(next_page):
            self.crawlerNext(conf,url=next_page)

# 测试字典采集
def runDict():
    pageDict = PageDict()
    start_url="http://www.xuexi111.org/about/sitemap.html"
    conf={
        "group":'*//div[@class="site-map"]/a',
        "columns":[
            {"名称": "主键", "规则": "md5", "类型": "主键","连接": "地址"},
            {"名称": "网站", "规则": "学习资料库", "类型": "不解析"},
            {"名称":"类别","规则":".//text()","类型":"文本"},
            {"名称": "地址", "规则": "./@href", "类型": "连接"},
            {"名称": "采集时间", "规则": "%Y.%m.%d %H:%M:%S", "类型": "采集时间"},
        ],
    }
    pageDict.runDict(url=start_url,conf=conf)


def runList():
    file_path = '../data/xuexi111.csv'
    pageDict = PageDict()
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
    pageDict.runList(file_path=file_path, confs=confs,dictconf=dictconf)

if __name__ == '__main__':
    #runDict()
    runList()
