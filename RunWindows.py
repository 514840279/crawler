# -*- coding: utf-8 -*-

import sys
from ui.Windows import Ui_MainWindow
from PyQt5 import QtWidgets
from ui.RunAbout import RunAbout
from ui.RunMainList import RunMainList
from ui.RunMainContext import RunMainContext
from PyQt5 import QtCore,QtGui
from PyQt5.QtGui import QFont

import time


class MenuLinsenWindow(Ui_MainWindow,QtWidgets.QMainWindow):


    # 初始化信息
    def __init__(self):
        super(MenuLinsenWindow,self).__init__()
        self.setupUi(self)

        # 添加布局
        formabout = RunAbout()
        self.stackedWidget.addWidget(formabout)
        mainList = RunMainList()
        self.stackedWidget.addWidget(mainList)
        mainContext = RunMainContext()
        self.stackedWidget.addWidget(mainContext)

        # menu 与 布局绑定
        self.actionLiebiao.triggered.connect(lambda: self.showPage(1))
        self.actionguanyu.triggered.connect(lambda: self.showPage(0))
        self.actionNeirong.triggered.connect(lambda: self.showPage(2))

        self.showPage(1)

    def showPage(self,index):
        self.stackedWidget.setCurrentIndex(index)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui =  MenuLinsenWindow()
    test = """ 
    # 创建QSplashScreen对象实例
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("uugai_94x194.png"))
    # 设置画面中的文字的字体
    splash.setFont(QFont('Microsoft YaHei UI', 12))
    #splash.setStyleSheet("#MainWindow{background-color: green}")
    # 显示画面
    splash.show()
    # 显示信息
    splash.showMessage("启动中... 0%", QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
    time.sleep(1)
    splash.showMessage("正在加载样式表...20%", QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
    #if (ui_style == 'dark'):
    #    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    time.sleep(1)
    splash.showMessage("正在加载样式表...40%", QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
    time.sleep(1)
    splash.showMessage("正在加载数据库配置...60%", QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
    time.sleep(1)
    splash.showMessage("正在测试数据库连接...80%", QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
    #conn = GetMysqlConnection().get_connection()
    #if (conn != 0):
    #    conn.close()
    #   splash.showMessage("正在测试数据库连接...Success", QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
    #else:
    #    splash.showMessage("正在测试数据库连接...faild", QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
    time.sleep(2)
    splash.showMessage("启动中...100%", QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
    time.sleep(1)

    # 当主界面显示后销毁启动画面
    splash.finish(ui)
    """
    ui.show()
    sys.exit(app.exec_())

