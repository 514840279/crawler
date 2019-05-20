# -*- coding: utf-8 -*-

import sys
from Windows import Ui_MainWindow
from PyQt5 import  QtCore,QtGui, QtWidgets
from common.HtmlSource import HtmlSource
from common.RuleConf import Rule
from lxml import html

import uuid



class BtnLinsenWindow(Ui_MainWindow,QtWidgets.QMainWindow):
    html_context = ""
    conf={
        "url":''  ,
        "body_content_xpath":"",
        "columns":[]
    }
    body_content_list = []

    def __init__(self):
        super(BtnLinsenWindow,self).__init__()
        self.setupUi(self)
        self.urlLineEdit.setText("http://www.xuexi111.org/yingyv/")
        # url 测试
        self.urlbutton.clicked.connect(self.openUrl)
        # body_content_xpath 测试
        self.pushButton.clicked.connect(self.testBody)
        # 列表配置测试
        self.pushButton_2.clicked.connect(self.testColumn)
        self.pushButton_7.clicked.connect(self.showTable)


    #定义槽函数 获取html页面
    def openUrl(self):
        self.conf["url"] = self.urlLineEdit.text()
        # 加载外部页面，调用
        #self.webEngineView.setUrl(QtCore.QUrl(url))
        print(self.conf["url"])
        htmlSource = HtmlSource()
        self.html_context = htmlSource.get_html(url_p=self.conf["url"],type_p='rg')
        self.textBrowser.setText(self.html_context)
        self.lineEdit.setText("// div[@class =\"padd w645\"]/div[@class=\"list_left\"]/div[@class=\"topic-list\"]/ul/li")

    # 定义槽函数 body 信息
    def testBody(self):
        self.conf["body_content_xpath"] = self.lineEdit.text()
        tree = html.fromstring(self.html_context)
        result_list = tree.xpath(self.conf['body_content_xpath'])
        if(len(result_list)>0):
            self.body_content_list =result_list
            self.lineEdit_3.setText('./h3/a/text()')
            # 其他按钮允许点击

    # 定义槽函数 列信息
    def testColumn(self):
        # 定义一个字段的读取配置
        self.column={
            "uuid":   uuid.uuid4(),
            "c_name":'',    # 必须
            "c_xpath":'',   # 必须
            "c_type":'',    # 必须
            "c_append_befor" :'',
            "c_append_after":'',
            "c_strart_index" :'',
            "c_end_len":'' ,
            "c_replace_char":''
        }
        self.column["c_name"] = self.lineEdit_2.text()
        self.column["c_xpath"] = self.lineEdit_3.text()
        self.column["c_type"] = self.comboBox.currentText()
        print(self.column)
        list=[]
        rule = Rule()
        for row in self.body_content_list:
            column_text = rule._analysis_(tree=row, column=self.column)
            list.append(column_text)
        if(len(list) == len(self.body_content_list)):
            self.conf['columns'].append(self.column)
            self.textBrowser.setText(str(list))


    # 预览信息
    def showTable(self):

        viewText = ''
        for column in self.conf['columns']:
            viewText = viewText + "\t" + column['c_name']
        viewText = viewText +"\r\n"
        rule = Rule()
        list = rule._analysis_list(list=self.body_content_list, columns=self.conf["columns"])

        for row in list:
            for column in self.conf['columns']:
                viewText = viewText + "\t" + str(row[column['c_name']])
            viewText = viewText + "\r\n"
        self.textBrowser.setText(viewText)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui =  BtnLinsenWindow()

    ui.show()
    sys.exit(app.exec_())

