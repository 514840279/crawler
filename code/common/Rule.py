#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import hashlib
from lxml import html


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

    # 数据提取详细页的
    def html_content_analysis_detial(self,html_text, column,url):
        md5 = self.get_md5_value(src=html_text)
        tree = html.fromstring(html_text)
        column_context = []
        #column_context = [("md5", [md5])]
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
                # 二次处理
                text = tree.xpath(a[1])
                print(text)
                if len(text)>0:
                    column_context.append((a[0], [(text[0].split(a[3])[a[4]]).strip()]))
                else:
                    column_context.append((a[0], []))
            elif 'sab' == a[2]:
                # 二次处理 字符串前拼接
                # 赶集网读取联系电话完整图片地址 处理过程
                text = tree.xpath(a[1])
                list = []
                for path in text:
                    list.append(a[3] + path.strip())
                column_context.append((a[0], list))
            elif 'sr' == a[2]:
                # 二次处理 字符串前拼接
                # 赶集网读取联系电话完整图片地址 处理过程
                text = tree.xpath(a[1])
                list = []
                for path in text:
                    list.append(self.get_url_root(url) + path.strip())
                column_context.append((a[0], list))
            elif 'arr' == a[2]:
                # 二次处理 几个中的一个
                text = tree.xpath(a[1])
                column_context.append((a[0], text[a[3]].strip()))
            elif 'sarr' == a[2]:
                # 二次处理 几个中的和成一个
                text = tree.xpath(a[1])
                st = ''
                for item in text:
                    #print(item)
                    if item.strip() == '':
                        pass
                    else:
                        st = st +item.strip()
                column_context.append((a[0], [st.strip()]))
            elif 'sarra' == a[2]:
                # 二次处理 几个中的和成一个
                text = tree.xpath(a[1])
                st = ''
                for item in text:
                    #print(item)
                    if item.strip() == '':
                        pass
                    else:
                        st = st +item.strip()+a[3]
                column_context.append((a[0], [st.strip()]))
            elif 'nsp' == a[2]:
                # 二次处理 非固定列 ul处理
                # 应届生网最后的不固定信息
                text = tree.xpath(a[1])
                list = []
                column = []
                for item in text:
                    print(item)
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
                # 拉钩网企业信息不固定
                text = tree.xpath(a[1])
                list = []
                column = []
                for item in text:
                    print(item)
                    if item.strip() == '':
                        pass
                    else:
                        list.append(item.strip())
                for item in range(len(list)):
                    if item % 2 == 1:
                        column.append(([list[item]], list[item - 1]))
                column_context.append((a[0], column))
                # print(a[0]+a[1]+a[2])
        return column_context

    # 数据提取列表页处理方式
    def html_content_analysis_list(self,html_text, column,url):
        column_content = self.html_content_analysis_detial(html_text, column, url)
        le = len(column_content)
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
                    listb.append((a[0], a[1][i]))
            lista.append(listb)
        return lista
