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

# III. 升级版
此版本高度封装，是操作简单使用方便，
```
from  common.RuleConf import *
def test():
    conf = {
        "urltable": "xuexi111_list",  # 地址来源表
        "urlname": '地址',  # 来源表的字段
        "tablename": "xuexi111_detail",  # 结果数据存入数据表
        "group": '*/div[@class="content"]',  # 数据在网页中展示的范围 xpath
        "readtype": 'rg',
        # 网页请求数据方式方法，默认是 rg，可选 rg （request get），rp （request post），se （Selenium  开发中），ul （urlllib） 后开发多种方式执行自动选择
                "pagetype": 'detail', #  区分网页的类型属于 dict（网站地图），list（数据列表），detail（详细信息）
        # "chartset":"gb2312", # 默认是 utf8
        "columns": [  # 数据表配置项，对应结果表的字段
            {"类型": "主键",  # 系统默认类型包括 主键，不解析，本地连接，采集时间，文本，连接，图片，数组，context，list
             "名称": "主键",  # 当类型为主键时，规则 可选uuid （随机生成），md5（必须有 连接 属性） 两种
             "规则": "md5",  # 规则一般使用 xpath 规则，极个别系统配置不采用xpath 比如主键，本地连接，采集时间，不解析（规则原文本返回），
             "连接": "地址"  # 除 类型，名称，规则 三个必须的属性外，其他会有额外的一些属性辅助，
                             # 例如  主键的md5必须有链接属性（属性值对应其他字段的名称），congtext 和 list代表包含更复杂的columns
             },
            {"类型": "不解析", "名称": "网站", "规则": "学习资料库"},
            {"类型": "本地连接", "名称": "地址", "规则": "", },
            {"类型": "采集时间", "名称": "采集时间", "规则": "%Y.%m.%d %H:%M:%S", },
            {"类型": "文本", "名称": "标题", "规则": "./h1/text()"},
            {"类型": "图片", "名称": "图片", "规则": './/div[@class="cont_l"]/div[@class="cont_lt"]/img/@src'},
            {"类型": "文本", "名称": "资料共享",
             "规则": './/div[@class="txt_info"]//div[@class="cont_l"]/div[@class="cont_lt"]/div[@class="cont_ltr"]/ul/li[1]/span//text()'},
            {"类型": "连接", "名称": "资料共享链接",
             "规则": './/div[@class="txt_info"]//div[@class="cont_l"]/div[@class="cont_lt"]/div[@class="cont_ltr"]/ul/li[1]/span/a/@href'},
            {"类型": "文本", "名称": "文件大小",
             "规则": './/div[@class="txt_info"]//div[@class="cont_l"]/div[@class="cont_lt"]/div[@class="cont_ltr"]/ul/li[2]/span//text()'},
            {"类型": "文本", "名称": "语言要求",
             "规则": './/div[@class="txt_info"]//div[@class="cont_l"]/div[@class="cont_lt"]/div[@class="cont_ltr"]/ul/li[3]/span//text()'},
            {"类型": "文本", "名称": "资料类型",
             "规则": './/div[@class="txt_info"]//div[@class="cont_l"]/div[@class="cont_lt"]/div[@class="cont_ltr"]/ul/li[4]/span//text()'},
            {"类型": "文本", "名称": "运行环境",
             "规则": './/div[@class="txt_info"]//div[@class="cont_l"]/div[@class="cont_lt"]/div[@class="cont_ltr"]/ul/li[5]/span//text()'},
            {"类型": "文本", "名称": "浏览次数",
             "规则": './/div[@class="txt_info"]//div[@class="cont_l"]/div[@class="cont_lt"]/div[@class="cont_ltr"]/ul/li[6]/span//text()'},
            {"类型": "文本", "名称": "更新时间",
             "规则": './/div[@class="txt_info"]//div[@class="cont_l"]/div[@class="cont_lt"]/div[@class="cont_ltr"]/ul/li[7]/span//text()'},
            {
                "名称": '资料介绍',
                "类型": 'context',
                "规则": './/div[@class="download"]/div[@class="download-left"]',
                "columns": [
                    {"名称": "资料介绍", "规则": './/div[@class="info-content"]', "类型": "源代码"},
                ]
            }, {
                "名称": '下载文件',
                "类型": 'list',
                "规则": './/div[@id="download"]/table//tr',
                "columns": [
                    {"名称": "文件名", "规则": './td[1]/a/text()', "类型": "文本"},
                    {"名称": "下载地址", "规则": './td[1]/a/@href', "类型": "连接"},
                    {"名称": "离线地址", "规则": './td[1]/div[@class="lixian-jpg"]/a/@href', "类型": "连接"},
                    {"名称": "文件大小", "规则": './td[@align="center"]/text()', "类型": "文本"},
                ]
            }
        ],
        "nextPage": '' # PageList 使用翻页配置 值用xpath配置 例如 '*//div[@class='pegebar']/a[@class='next']/@href'
    }
    
    pageCrawler = PageCrawler()
    pageCrawler.run(conf=conf)  # 使用run方法即可执行采集任务，
    
    # 使用 from  common.RuleConf import * 导入，根据判读要采集页面的类型使用那个 PageDict（采集网站地图和列表数据使用）PageList（采集列表数据使用） PageDetail（采集详细信息页面）
    #pageDetail = PageDetail() 
    #pageDetail.run(conf)    
    
    #pageList = PageList()
    #pageList.run(conf)
    
    #pageDict = PageDict()
    #pageDict.run(url=start_url, conf=conf) # url 代表网页 一般网站地图只一个页面，所以不需要配置来源表
```


本程序github：

	https://github.com/514840279/crawler


## 发展 
    crawler 开发至今不得不进行一项重大决定，基于使用人群扩大必须适用更广泛的人群设计。因此基于发展原则，需要构建ui以供更多的人使用，
    由于技术限制，现在开发仅仅提供xpath方式手动添加规则到文件中，假如技术难题解决将使用鼠标选择方式，以适用更广泛的人群。
    
    ui使用pyqt5构建，采用ui与逻辑分离方式快速描写ui，使用主窗体添加方式将多个子窗体包含进窗口中。
    
## 打包
    # 更新到最新的 pyinstaller
    pip install --upgrade pyinstaller
    # 进行打包
    pyinstaller -F -w -i favicon_32x32.ico -n 爬虫管理  RunWindows.py
    # 打包不包含图片，和配置文件以及生成文件的目录需要复制到一起
      打包完成后 在dist 中生成RunWindows.exe 双击即可执行
    -F 合并文件为一个
    -w 隐藏windows命令窗口
    -i 添加桌面图标，格式ico
    -n 命名程序名称 不允许使用中文，报gbk错误,可以修改代码
     C:\ProgramData\Anaconda3\Lib\site-packages\PyInstaller\utils\win32\winmanifest.py
     line:1075 with open(filename) as f: 添加参数 with open(filename,encoding="UTF-8") as f:
    
    
    
# pycharm 配置pyqt工具

    -- QtDesigner
    Name = QtDesigner
    Description = Qt tool for designing and building GUIs with Qt Widgets
    Program = C:\ProgramData\Anaconda3\Library\bin\designer.exe
    Arguments =     
    Working directory = $FileDir$
    
    -- PyUiCompiler
    Name = PyUiCompiler
    Description = Python User Interface Compiler for Qt
    Program = C:\ProgramData\Anaconda3\python.exe
    Arguments = -m PyQt5.uic.pyuic $FileName$ -o $FileNameWithoutExtension$.py    
    Working directory = $FileDir$
    
    -- Pyrcc
    Name = pyrcc
    Description = Python User Interface Compiler for Qt
    Program = C:\ProgramData\Anaconda3\Scripts\pyrcc5.exe
    Arguments = $FileName$ -o $FileNameWithoutExtension$_rc.py    
    Working directory = $FileDir$
    

    pip install pyqt=5.9.2
    pip install pyqt5=5.11.3
    pip install pyqt5-tools=5.11.3.1.4	
    
    