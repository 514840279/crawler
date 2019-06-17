# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget,QDialog
from ui.mainContext import Ui_Form
from ui.RunMainContextSub import RunMainContextSub
from common.HtmlSource import HtmlSource

import time
import uuid

class RunMainContext(QWidget, Ui_Form):
    conf = {
        "urlList": []
    }
    contexSub={

    }
    def __init__(self):
        super(RunMainContext, self).__init__()
        self.setupUi(self)
        # 隐藏
        self.tableWidget.setVisible(False)
        self.textBrowser.setVisible(False)

        # 初始化值 后期 修改变量
        self.textEdit.setText("""http://www.xuexi111.org/yingyv/yvfa/132324.html
http://www.xuexi111.org/yingyv/fangfa/132203.html
http://www.xuexi111.org/yingyv/cet46/132169.html
http://www.xuexi111.org/yingyv/cihui/132131.html
http://www.xuexi111.org/yingyv/xiezuo/131994.html
http://www.xuexi111.org/yingyv/cihui/131829.html
http://www.xuexi111.org/yingyv/xiezuo/131615.html
http://www.xuexi111.org/yingyv/fangfa/131614.html
http://www.xuexi111.org/yingyv/kouyv/131613.html
http://www.xuexi111.org/yingyv/kouyv/131601.html
http://www.xuexi111.org/yingyv/kouyv/130483.html
http://www.xuexi111.org/yingyv/kouyv/130482.html
http://www.xuexi111.org/yingyv/tingli/130481.html
http://www.xuexi111.org/yingyv/liuxue/130480.html
http://www.xuexi111.org/yingyv/xiezuo/130479.html
http://www.xuexi111.org/yingyv/cihui/130478.html
http://www.xuexi111.org/yingyv/cihui/130477.html
http://www.xuexi111.org/yingyv/fangfa/130257.html
http://www.xuexi111.org/yingyv/tingli/130218.html
http://www.xuexi111.org/yingyv/yuedu/130217.html
""")

        # 绑定事件
        self.pushButton.clicked.connect(self.openUrl)
        self.pushButton_3.clicked.connect(self.addContextSub)

    # 定义槽函数 获取html页面
    def openUrl(self):
        self.conf["urlList"] = self.textEdit.toPlainText().split("\n") # 获取文本用toPlainText
        self.textBrowser.setVisible(True)
        htmlSource = HtmlSource()
        html_context = htmlSource.get_html(url_p=self.conf["urlList"][0], type_p='rg')
        self.textBrowser.setText(html_context)

    def showSubDialog(self):
        # 因为使用Qt Designer设计的ui是默认继承自object类，不提供show()显示方法，
        # 所以我们需要生成一个QDialog对象来重载我们设计的Ui_Dialog类，从而达到显示效果。
        MainDialog = QDialog()  # 创建一个主窗体（必须要有一个主窗体）
        myDialog = RunMainContextSub.Ui_Dialog()  # 创建对话框
        myDialog.setupUi(MainDialog)  # 将对话框依附于主窗体
        # 设置窗口的属性为ApplicationModal模态，用户只有关闭弹窗后，才能关闭主界面
        # MainDialog.setWindowModality(Qt.ApplicationModal)
        MainDialog.show()

    # 定义槽函数 列添加配置信息
    def addContextSub(self):
        # 判断填写规则不为空
        if (self.column['规则'] == ""):
            return
        # 判断列名称 不为空
        if (self.column['名称'] == ""):
            return

        flag = True
        for t_column in self.conf["columns"]:
            if (t_column['uuid'] == self.column['uuid']):
                flag = False
                t_column = self.column
            elif (t_column['名称'] == self.column['名称']):
                # 同名不同id 的应该给出提示
                flag = False
                t_column = self.column
        if (flag == True):
            self.conf['columns'].append(self.column)

            # 初始化配置
            self.lineEdit_3.setText('')
            self.lineEdit_2.setText('')
            self.column = {
                "uuid": str(uuid.uuid4()),
                "名称": '',  # 必须
                "规则": '',  # 必须
                "类型": '',  # 必须
                "c_append_befor": '',
                "c_append_after": '',
                "c_strart_index": '',
                "c_end_len": '',
                "c_replace_char": ''
            }
            self.lineEdit_2.setText('连接')
            self.lineEdit_3.setText('./h3/a/@href')
            self.comboBox.setCurrentText("连接")

        # 动态展示添加好的列配置，并绑定删除 TODO

        # 更新配置展示
        self.showColumns()

        # 更新表格数据
        self.showTable()