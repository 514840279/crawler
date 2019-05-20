#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from lxml import etree

class Rule:

    # 解析列表页面
    def _analysis_list(self, list, columns):
        list_context=[]
        for tree in list:
            list_context.append(self._analysis_context(tree=tree,columns=columns))
        return list_context

    # 解析页面
    def _analysis_context(self, tree, columns):
        columns_context ={}
        for column in columns:
            columns_context[column["c_name"]] = self._analysis_(tree=tree,column=column)
        return columns_context

    # 解析页面
    def _analysis_(self, tree, column):
        column_context=''
        if '文本' == column["c_type"]:
            # 进行lxml方式解析
            column_context= tree.xpath(column["c_xpath"])[0]
        return column_context




