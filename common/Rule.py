#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import hashlib
from lxml import html

import re

class Rule:
    # 计算MD5值
    def get_md5_value(self,src):
        myMd5 = hashlib.md5()
        myMd5.update(src.encode("utf8"))
        myMd5_Digest = myMd5.hexdigest()
        return myMd5_Digest

    # 读取网站域名
    def get_url_root(self, url):
        http = ''
        https = ''
        url_root = ''
        if 'http://' in url or 'http:/' in url:
            http = 'http://'
            url = url.replace('http://', '').replace('http:/', '').strip()
        elif 'https://' in url or 'https:/' in url:
            https = 'https://'
            url = url.replace('https://', '').replace('httpss:/', '').strip()
        else:
            pass
        url_root = url.split('/')[0]
        return (http + https + url_root)



    # 解析页面
    def _analysis_(self, tree, column,url):
        column_context = []
        # column_context = [("md5", [md5])]
        # column_context.append(("标题链接", [url]))
        for a in column:
            if 'l' == a[2]:
                # 进行lxml方式解析
                text = tree.xpath(a[1])
                column_context.append((a[0], text))
            elif 'n' == a[2]:
                # 返回 做补位处理
                column_context.append((a[0], [a[1]]))
            elif 'sp' == a[2]:
                # split 分割字符串取其中一个
                text = tree.xpath(a[1])
                if len(text) > 0:
                    column_context.append((a[0], [(text[0].split(a[3])[a[4]]).strip()]))
                else:
                    column_context.append((a[0], []))
            elif 'sab' == a[2]:
                #  多个字符串 后拼接
                text = tree.xpath(a[1])
                list = []
                for path in text:
                    if(len(path.strip())>0):
                        list.append(a[3] + path.strip())
                column_context.append((a[0], list))
            elif 'arr' == a[2]:
                # 数组中取其中一个
                text = tree.xpath(a[1])
                if (len(text) == 0 or len(text) < a[3]):
                    if (len(text) == 0):
                        column_context.append((a[0], text))
                    else:
                        column_context.append((a[0], text.strip()))
                else:
                    column_context.append((a[0], [text[a[3]].strip()]))
            elif 'sarrsub' == a[2]:
                # 数组拼接成字符串截取部分
                text = tree.xpath(a[1])
                st = ''
                for item in text:
                    # print(item)
                    if item.strip() != '':
                        st = st + item.strip()
                column_context.append((a[0], [st.strip()]))
            elif 'sarr' == a[2]:
                # 数组拼接成字符串
                text = tree.xpath(a[1])
                st = ''
                for item in text:
                    # print(item)
                    if item.strip() != '':
                        st = st + item.strip()
                column_context.append((a[0], [st.strip()]))
            elif 'nsp' == a[2]:
                # 二次处理 非固定列 ul处理
                # 集合中单数做列，双数做数据
                text = tree.xpath(a[1])
                list = []
                column = []
                for item in text:
                    if item.strip() == '':
                        pass
                    else:
                        list.append(item.strip())
                for item in range(len(list)):
                    if item % 2 == 1:
                        column.append((list[item - 1], [list[item]]))
                column_context.append((a[0], column))
            elif 'nspa' == a[2]:
                # 二次处理 非固定列 ul处理
                # 拉钩网企业信息不固定，集合中单数做数据，双数做列
                text = tree.xpath(a[1])
                list = []
                column = []
                for item in text:
                    if item.strip() == '':
                        pass
                    else:
                        list.append(item.strip())
                for item in range(len(list)):
                    if item % 2 == 1:
                        column.append(([list[item]], list[item - 1]))
                column_context.append((a[0], column))
                # print(a[0]+a[1]+a[2])

            elif 'sarr-reg'== a[2]:
                # 正则： 拼接后截取
                text = tree.xpath(a[1])
                st = ''
                for item in text:
                    if item.strip() == '':
                        pass
                    else:
                        st = st + item.strip()
                st = re.sub(r''+a[3],'',st.strip(),0,re.S)
                column_context.append((a[0], [st.strip()]))
            elif 'arr-reg' == a[2]:
                # 正则： 获取集合每个分别截取
                text = tree.xpath(a[1])
                list = []
                for item in text:
                    if item.strip() == '':
                        pass
                    else:
                        list.append(re.sub(r'' + a[3], '', item.strip(), 0, re.S).strip())
                column_context.append((a[0], list))
            elif 'reg' == a[2]:
                # 正则： 获取
                text = tree.xpath(a[1])
                st = ''
                for item in text:
                    if item.strip() == '':
                        pass
                    else:
                        st = st + item.strip()
                pattern = re.compile(r'' + a[3])  # 查找数字
                result1 = pattern.findall(st)
                column_context.append((a[0], result1))
            elif 'arr-replace' == a[2]:
                # 数组每个都替换特定字符串
                text = tree.xpath(a[1])
                list = []
                for item in text:
                    if str(item.strip()).replace(a[3],"") == '':
                        pass
                    else:
                        list.append(str(item.strip()).replace(a[3],"").strip())
                column_context.append((a[0], list))
        return column_context

    # 数据提取详细页的
    def html_content_analysis_detial(self,html_text, column,url):
        # md5 = self.get_md5_value(src=html_text)
        tree = html.fromstring(html_text)
        return self._analysis_(tree=tree,column=column,url=url)

    # 数据提取列表页处理方式
    def html_content_analysis_list(self,html_text, column,url):
        column_content = self.html_content_analysis_detial(html_text, column, url)
        c = column_content[0][1]
        lista = []
        for i in range(len(c)):
            listb=[]
            for a in column_content:
                if a[0] == '标题链接':
                    continue
                if len(a[1]) < len(c):
                    listb.append(a)
                else:
                    listb.append((a[0], str(a[1][i]).strip()))
            lista.append(listb)
        return lista


    # 数据提取列表页处理方式
    def html_content_analysis_list2(self,html_text,group, column,url):
        tree = html.fromstring(html_text)
        column_content =  self._analysis_(tree=tree, column=group, url=url)
        #htmlsource = HtmlSource()
        #nextpage = htmlsource.addr_reckon(nextpage)
        lista = []
        for a in range(len(column_content[0][1])):
            row = self._analysis_(tree=column_content[0][1][a], column=column,url=url)
            lista.append(row)
        print(lista)
        return lista