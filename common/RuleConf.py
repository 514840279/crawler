#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from lxml import etree,html
from common.HtmlSource import HtmlSource
from urllib import parse

import hashlib
import uuid
import time


class Rule:

    # 采集列表页面
    def crawler_list(self,url,conf):
        htmlSource = HtmlSource()
        # 获取网页原文
        html_context = htmlSource.get_html(url_p=url)
        index =0
        while(len(html_context)<128 and index<2):
            html_context = htmlSource.get_html(url_p=url)
            index+=1
        if(len(html_context)<128):
            raise Exception('网页访问失败，无内容！')
        # 解析原文
        tree = html.fromstring(html_context)
        result_list = tree.xpath(conf['group'])
        result_list_context = self._analysis_list(list=result_list, columns=conf['columns'],url=url)
        if(conf['nextPage']):
            next_page = tree.xpath(conf['nextPage'])
            if(len(next_page)>0):
                return result_list_context,next_page[0]
            else:
                return result_list_context,None
        else:
            return result_list_context,None

    # 解析列表页面
    def _analysis_list(self, list, columns,url=""):
        list_context=[]
        for tree in list:
            list_context.append(self._analysis_context(tree=tree,columns=columns,url=url))
        return list_context

    def crawler_detail(self, confs, url=''):
        htmlSource = HtmlSource()
        # 获取网页原文
        html_context = htmlSource.get_html(url_p=url)
        # 解析原文
        tree = html.fromstring(html_context)
        result = {}
        for conf in confs['group']:
            if (conf['groupType'] == 'detail'):
                detailTree = tree.xpath(conf["group"])[0]
                result[conf['groupName']] = self._analysis_context(tree=detailTree,columns=conf['columns'],url=url)
            elif (conf['groupType'] == 'list'):
                listTree = tree.xpath(conf["group"])
                result[conf['groupName']] = self._analysis_list(list=listTree,columns=conf['columns'],url=url)
        return result

    # 解析页面
    def _analysis_context(self, tree, columns ,url=""):
        columns_context ={}
        id_flag= False
        for column in columns:
            if('主键' == column["类型"]):
                column_id = column
                id_flag = True
            else:
                # 除主键其他数据解析
                columns_context[column["名称"]] = self._analysis_(tree=tree,column=column,url=url)
        # 主键解析
        if(id_flag):
            if ('md5' == column_id["规则"]):
                column_id["url"] = columns_context[column_id["连接"]]
            columns_context[column_id["名称"]] = self._analysis_(tree=tree, column=column_id, url=url)
        return columns_context

    # 解析页面
    def _analysis_(self, tree, column,url=""):
        column_context=''
        if column["类型"] == '主键':
            # 不同的主键策略 默认使用uuid
            if('uuid' == column["规则"]):
                column_context = str(uuid.uuid4()).replace("-",'')
            elif ('md5' == column["规则"]):
                myMd5 = hashlib.md5()
                myMd5.update(column["url"].encode("utf8"))
                myMd5_Digest = myMd5.hexdigest()
                column_context = myMd5_Digest
            else:
                column_context = uuid.uuid4()
        if column["类型"] == '不解析':
            # 返回填写的规则原文
            column_context = column["规则"]
        if column["类型"] == '文本':
            # 进行lxml方式解析
            text=''
            for a in tree.xpath(column["规则"]):
                text=text+str(a).strip()
            column_context = text
        if column["类型"] == '连接':
            # 进行lxml方式解析
            imgurl =tree.xpath(column["规则"])
            if len(imgurl) > 1:
                imgs =[]
                for img in imgurl:
                    imgs.append(parse.urljoin(url, img))
                column_context = imgs
            elif (len(imgurl) == 1):
                column_context = parse.urljoin(url, imgurl[0])
            else:
                column_context = ''
        if column["类型"] == '图片':
            # 进行lxml方式解析
            imgs = tree.xpath(column["规则"])
            if len(imgs)>1:
                column_context =  imgs
            elif(len(imgs)==1):
                column_context = imgs[0]
            else:
                column_context=''
        if column["类型"] == '采集时间':
            # 系统当前时间
            rg = '%Y.%m.%d %H:%M:%S'
            if column["规则"]!='':
                rg = column["规则"]
            column_context = time.strftime(rg,time.localtime(time.time()))
        if column["类型"] == '源代码':
            # 进行lxml方式解析
            html_context = tree.xpath(column["规则"])
            html_str=''
            for content in html_context:
                strs = etree.tostring(content,encoding = "utf-8", pretty_print = True, method = "html").decode("utf-8")  # 转为字符串
                html_str = html_str+ strs
            column_context = html_str
        if column["类型"] == '本地连接':
            # 进行lxml方式解析
            column_context = url
        return column_context



if __name__ == '__main__':
    pass
