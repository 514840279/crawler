# -*- coding: utf-8 -*-

import sys
from Windows import Ui_MainWindow
from PyQt5 import  QtCore,QtGui, QtWidgets


class BtnLinsenWindow(Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self):
        super(BtnLinsenWindow,self).__init__()
        self.setupUi(self)
        self.urlLineEdit.setText("http://www.xuexi111.org/yingyv/")
        self.urlbutton.clicked.connect(self.openUrl)

    #定义槽函数
    def openUrl(self):
        url = self.urlLineEdit.text()
        # 加载外部页面，调用
        self.webEngineView.setUrl(QtCore.QUrl(url))





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui =  BtnLinsenWindow()
    ui.show()
    sys.exit(app.exec_())



