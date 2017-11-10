# 环境搭建
本系统依据python3.4.4进行开发的
其他依赖模块如下：
* pymysql
* lxml （这个使用pip 直接安装并不能安装成功，使用已经编译好的/model/lxml-3.7.3-cp34-cp34m-win_amd64.whl 安装，
安装方法：cd model
 pip install lxml-3.7.3-cp34-cp34m-win_amd64.whl
 ）
 * requests
 * BeautifulSoup4
 * selenium
各位在执行本系统前 需要将以上依赖依次安装，安装方法：（ pip3 install 模块名 ）

#crawler 网络爬虫
本项目是ldae工作室的定制爬虫项目
仅供个人开发学习，拒绝一切商业目的

## 文件介绍
1. application.py 	程序的入口
2. Currency.py		通用网页采集程序
3. z_code_*.py		特殊网页采集程序（独立程序）
4. HtmlSource.py 	网页采集程序
5. ResultData.py 	数据结果入库
6. Rule.py		网页数据提取
7. chromedriver.exe,IEDriverServer.exe,phantomjs.exe 浏览器驱动程序，浏览器模拟使用


## 采集流程
I. application：

1. 读取所有配置信息
2. 读取网页地址列表
3. 判断每一个地址是否有配置信息
4. 如果有进入采集程序
    
		获取网页源码（HtmlSource）
		粗提取url
		判断url是否当前的网站内地址
		如果是入库标记状态0
		如果不是丢弃url
		将网页源码和当前url传递给（Rule）获得结果
		调用ResultData入库
5. 如果没有自动添加新的配置信息，并提示用户进行修改

II. Currency:

1. 接受要采集的种子信息和地址信息，
2. 判读有配置模板信息
3. 如果有调用网页采集程序，调用规则提取数据，调用结果配置数据入库，完成采集任务

III. z_code_*:

1. 根据不同配置，调用不同的采集程序
2. 采集特殊程序与通用行程序没有关联，

## 规则介绍
IV. HtmlSource:

1. 获取参数请求方式，字符编码。
2. 根据参数采用不同的请求方式得到源码。
3. 请求方式可分为 requests.post,requests.get,builtfulsoup,url.open,webdriver等。
4. 获取网页字符集自动判断补充配置


V. Rule:

1. 获取网页源码。
2. 获取提取数据的配置
3. 提取配置的方式可分为 

		n 	直接返回字符串。
		l 	按规则提取数据。
		arr 	从结果结合中提取一个元素作为最终结果。
		sarr	按规则提取数据,数组集合合并为单一字符串并返回。
		sarra	按规则提取数据,数组集合拼接字符串合并为单一字符串并返回。
		sp	分割字符串取结果中一个作为最终结果。
		app 	从结果字符串的前（后）拼接一个固定字符串作为最终结果。
		nsp 	结果数组中奇数作为key，偶数作为value。
		spa	结果数组中偶数作为key，奇数作为value。
		str 	结果字符中截取一段作为最终的结果
		rep 	结果字符串替换掉一些无用的字符串
4. 返回结果有一些固定值。例如 md5(网页源码的值)，信息来源（网页url），采集时间（当前系统时间）
5. 返回结果组装成元祖集合形如：[("md5","12346"),("信息来源","天天无忧"),("URL","http://")]

VI. ResultData:

1. 获取参数结果
2. 读取结果配置信息
3. 拼接sql
4. 直接入库完成采集

## 二次开发
I.基于通用程序进行快速二次开发流程

1. 编写入口URL的规则
2. 编写list页面的规则
3. 编写详细页面信息的读取规则

II. 模板

```
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.HtmlSource import HtmlSource
from common.Rule import Rule
from common.inc_conn import Conn_mysql

htmlSource = HtmlSource()
rule = Rule()
ldae_mysql = Conn_mysql( host='localhost', user='root', passwd='root', db='ldae', port=3306) # 生成MYSQL数据库索引数据实例

# 详细页面读取规则
def read_detial(url,type):
    detial_html = htmlSource.get_html(url_p=url, type_p='rg')
    #print(detial_html)
    colum=[
        ('title','//div[@class="ui-grid ui-main clearfix"]//div[@class="bread-crumb-spacial"]//span[@class="title"]//text()','l'),
        ('content','//div[@class="main-wrap"]//div[@class="problem-detail-wrap"]//div[@class="block-line"]//div[@class="context-left"]//text()','sarra',',')
   ]
    result = rule.html_content_analysis_detial(html_text=detial_html, column=colum, url=url)
    #print(result)
    sql="insert into cancer value('%s','%s','%s','%s','%s')"%(result[0][1][0],str(result[1][1][0]).replace('患者,图片因隐私问题无法显示','').replace("患者,","患者:").replace("医生,","医生:").replace('\'','"'),type,'春雨医生',url)
    print(sql)
    ldae_mysql.write_sql(sql=sql)

# 入口url规则，list a标签读取贵州
def main():
    start_url = "https://www.chunyuyisheng.com/pc/search/qalist/?query=%s&page=%d"
    str = ["肺癌"," 肝癌","乳腺癌","胃癌","直肠癌"] 
    for ss in str:
        for i in range(1,51):
            url = start_url%(ss,i)
            #print(url)
            list_html = htmlSource.get_html(url_p=url,type_p='rg')
            #print(list_html)
            colum=[('a','//div[@class="hot-qa main-block"]//div//div[@class="qa-item qa-item-ask"]//a//@href','sab','https://www.chunyuyisheng.com')]
            list = rule.html_content_analysis_detial(html_text=list_html,column=colum,url=url)
            print(list)
            for a in list[0][1]:
                read_detial(a, ss)
                #th = threading.Thread(target=read_detial, args=(a,str))
                #th.start()  # 启动线程


if __name__ == '__main__': # 判断文件入口
    main()

```



本程序github：

	https://github.com/514840279/crawler

前台程序：

	https://github.com/514840279/danyuan-application

交qq流群： 

	180307529
