# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Windows.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(920, 705)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("favicon_32x32.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolTipDuration(-1)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 920, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.actionjiankong = QtWidgets.QAction(MainWindow)
        self.actionjiankong.setObjectName("actionjiankong")
        self.actionLiebiao = QtWidgets.QAction(MainWindow)
        self.actionLiebiao.setObjectName("actionLiebiao")
        self.actionNeirong = QtWidgets.QAction(MainWindow)
        self.actionNeirong.setObjectName("actionNeirong")
        self.actionguanyuwomen = QtWidgets.QAction(MainWindow)
        self.actionguanyuwomen.setObjectName("actionguanyuwomen")
        self.actionguanyu = QtWidgets.QAction(MainWindow)
        self.actionguanyu.setObjectName("actionguanyu")
        self.actioncaiji = QtWidgets.QAction(MainWindow)
        self.actioncaiji.setObjectName("actioncaiji")
        self.actionrenwu = QtWidgets.QAction(MainWindow)
        self.actionrenwu.setObjectName("actionrenwu")
        self.actionshuju = QtWidgets.QAction(MainWindow)
        self.actionshuju.setObjectName("actionshuju")
        self.menu.addAction(self.actionLiebiao)
        self.menu.addAction(self.actionNeirong)
        self.menu_2.addAction(self.actionguanyu)
        self.menu_3.addAction(self.actioncaiji)
        self.menu_3.addAction(self.actionjiankong)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "爬虫管理"))
        self.menu.setTitle(_translate("MainWindow", "创建"))
        self.menu_2.setTitle(_translate("MainWindow", "关于我们"))
        self.menu_3.setTitle(_translate("MainWindow", "分析"))
        self.actionjiankong.setText(_translate("MainWindow", "监控"))
        self.actionLiebiao.setText(_translate("MainWindow", "列表"))
        self.actionNeirong.setText(_translate("MainWindow", "内容"))
        self.actionguanyuwomen.setText(_translate("MainWindow", "关于我们"))
        self.actionguanyu.setText(_translate("MainWindow", "关于我们"))
        self.actioncaiji.setText(_translate("MainWindow", "每日数据"))
        self.actionrenwu.setText(_translate("MainWindow", "renwu"))
        self.actionshuju.setText(_translate("MainWindow", "shuju"))

