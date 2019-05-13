import urllib.request
from urllib import parse
from lxml import etree
#import ssl
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QTextEdit, QVBoxLayout, QPushButton, QMessageBox
import sys

# 取消代理验证
#ssl._create_default_https_context = ssl._create_unverified_context

class TextEditMeiJu(QWidget):
    def __init__(self, parent=None):
        super(TextEditMeiJu, self).__init__(parent)
        # 定义窗口头部信息
        self.setWindowTitle('美剧天堂')
        # 定义窗口的初始大小
        self.resize(500, 600)
        # 创建单行文本框
        self.textLineEdit = QLineEdit()
        # 创建一个按钮
        self.btnButton = QPushButton('确定')
        # 创建多行文本框
        self.textEdit = QTextEdit()
        # 实例化垂直布局
        layout = QVBoxLayout()
        # 相关控件添加到垂直布局中
        layout.addWidget(self.textLineEdit)
        layout.addWidget(self.btnButton)
        layout.addWidget(self.textEdit)
        # 设置布局
        self.setLayout(layout)
        # 将按钮的点击信号与相关的槽函数进行绑定，点击即触发
        self.btnButton.clicked.connect(self.buttonClick)

    # 点击确认按钮
    def buttonClick(self):
        # 爬取开始前提示一下
        start = QMessageBox.information(
            self, '提示', '是否开始爬取《' + self.textLineEdit.text() + "》",
            QMessageBox.Ok | QMessageBox.No, QMessageBox.Ok
        )
        # 确定爬取
        if start == QMessageBox.Ok:
            self.page = 1
            self.loadSearchPage(self.textLineEdit.text(), self.page)
        # 取消爬取
        else:
            pass

    # 加载输入美剧名称后的页面
    def loadSearchPage(self, name, page):
        # 将文本转为 gb2312 编码格式
        name = parse.quote(name.encode('gb2312'))
        # 请求发送的 url 地址
        url = "https://www.meijutt.com/search/index.asp?page=" + str(page) + "&searchword=" + name + "&searchtype=-1"
        # 请求报头
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
        # 发送请求
        request = urllib.request.Request(url, headers=headers)
        # 获取请求的 html 文档
        html = urllib.request.urlopen(request).read()
        # 对 html 文档进行解析
        text = etree.HTML(html)
        # xpath 获取想要的信息
        pageTotal = text.xpath('//div[@class="page"]/span[1]/text()')
        # 判断搜索内容是否有结果
        if pageTotal:
            self.loadDetailPage(pageTotal, text, headers)
        # 搜索内容无结果
        else:
            self.infoSearchNull()

    # 加载点击搜索页面点击的本季页面
    def loadDetailPage(self, pageTotal, text, headers):
        # 取出搜索的结果一共多少页
        pageTotal = pageTotal[0].split('/')[1].rstrip("页")
        # 获取每一季的内容（剧名和链接）
        node_list = text.xpath('//a[@class="B font_14"]')
        items = {}
        items['name'] = self.textLineEdit.text()
        # 循环获取每一季的内容
        for node in node_list:
            # 获取信息
            title = node.xpath('@title')[0]
            link = node.xpath('@href')[0]
            items["title"] = title
            # 通过获取的单季链接跳转到本季的详情页面
            requestDetail = urllib.request.Request("https://www.meijutt.com" + link, headers=headers)
            htmlDetail = urllib.request.urlopen(requestDetail).read()
            textDetail = etree.HTML(htmlDetail)
            node_listDetail = textDetail.xpath('//div[@class="tabs-list current-tab"]//strong//a/@href')
            self.writeDetailPage(items, node_listDetail)
        # 爬取完毕提示
        if self.page == int(pageTotal):
            self.infoSearchDone()
        else:
            self.infoSearchContinue(pageTotal)

    # 将数据显示到图形界面
    def writeDetailPage(self, items, node_listDetail):
        for index, nodeLink in enumerate(node_listDetail):
            items["link"] = nodeLink
            # 写入图形界面
            self.textEdit.append(
                "<div>"
                    "<font color='black' size='3'>" + items['name'] + "</font>" + "\n"
                    "<font color='red' size='3'>" + items['title'] + "</font>" + "\n"
                    "<font color='orange' size='3'>第" + str(index + 1) + "集</font>" + "\n"
                    "<font color='green' size='3'>下载链接：</font>" + "\n"
                    "<font color='blue' size='3'>" + items['link'] + "</font>"
                    "<p></p>"
                "</div>"
            )

    # 搜索不到结果的提示信息
    def infoSearchNull(self):
        QMessageBox.information(
            self, '提示', '搜索结果不存在，请重新输入搜索内容',
            QMessageBox.Ok, QMessageBox.Ok
        )

    # 爬取数据完毕的提示信息
    def infoSearchDone(self):
        QMessageBox.information(
            self, '提示', '爬取《' + self.textLineEdit.text() + '》完毕',
            QMessageBox.Ok, QMessageBox.Ok
        )

    # 多页情况下是否继续爬取的提示信息
    def infoSearchContinue(self, pageTotal):
        end = QMessageBox.information(
            self, '提示', '爬取第' + str(self.page) + '页《' + self.textLineEdit.text() + '》完毕，还有' + str(int(pageTotal) - self.page) + '页，是否继续爬取',
            QMessageBox.Ok | QMessageBox.No, QMessageBox.No
        )
        if end == QMessageBox.Ok:
            self.page += 1
            self.loadSearchPage(self.textLineEdit.text(), self.page)
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TextEditMeiJu()
    win.show()
    sys.exit(app.exec_())