# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainList.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(918, 697)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(60, 0))
        self.label.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setMinimumSize(QtCore.QSize(60, 0))
        self.pushButton_3.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 2, 5, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setMinimumSize(QtCore.QSize(60, 0))
        self.pushButton.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 5, 1, 1)
        self.urlbutton = QtWidgets.QPushButton(Form)
        self.urlbutton.setMinimumSize(QtCore.QSize(60, 0))
        self.urlbutton.setMaximumSize(QtCore.QSize(80, 16777215))
        self.urlbutton.setObjectName("urlbutton")
        self.gridLayout.addWidget(self.urlbutton, 0, 5, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 2, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setMinimumSize(QtCore.QSize(60, 0))
        self.pushButton_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 4, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 3, 0, 1, 6)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMinimumSize(QtCore.QSize(60, 0))
        self.label_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)
        self.urlLineEdit = QtWidgets.QLineEdit(Form)
        self.urlLineEdit.setObjectName("urlLineEdit")
        self.gridLayout.addWidget(self.urlLineEdit, 0, 0, 1, 5)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 4)
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setMinimumSize(QtCore.QSize(60, 0))
        self.pushButton_4.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 5, 4, 1, 1)
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setMinimumSize(QtCore.QSize(60, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(80, 16777215))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 2, 3, 1, 1)
        self.saveConf = QtWidgets.QPushButton(Form)
        self.saveConf.setMinimumSize(QtCore.QSize(60, 0))
        self.saveConf.setMaximumSize(QtCore.QSize(80, 16777215))
        self.saveConf.setObjectName("saveConf")
        self.gridLayout.addWidget(self.saveConf, 7, 5, 1, 1)
        self.nextPage = QtWidgets.QPushButton(Form)
        self.nextPage.setMinimumSize(QtCore.QSize(60, 0))
        self.nextPage.setMaximumSize(QtCore.QSize(80, 16777215))
        self.nextPage.setObjectName("nextPage")
        self.gridLayout.addWidget(self.nextPage, 5, 5, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(400, 0))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 2)
        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 5, 1, 1, 2)
        self.comboBox_2 = QtWidgets.QComboBox(Form)
        self.comboBox_2.setMinimumSize(QtCore.QSize(60, 0))
        self.comboBox_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout.addWidget(self.comboBox_2, 5, 3, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setMinimumSize(QtCore.QSize(1, 0))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_2.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.tableView = QtWidgets.QTableView(Form)
        self.tableView.setShowGrid(False)
        self.tableView.setObjectName("tableView")
        self.gridLayout_2.addWidget(self.tableView, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "列表区域"))
        self.pushButton_3.setText(_translate("Form", "添加"))
        self.pushButton.setText(_translate("Form", "测试"))
        self.urlbutton.setText(_translate("Form", "获取源码"))
        self.lineEdit_2.setText(_translate("Form", "标题名"))
        self.pushButton_2.setText(_translate("Form", "测试"))
        self.label_2.setText(_translate("Form", "下一页"))
        self.urlLineEdit.setText(_translate("Form", "请输入列表页面的网址"))
        self.lineEdit.setText(_translate("Form", "请输入正确范围的xpath"))
        self.pushButton_4.setText(_translate("Form", "测试"))
        self.comboBox.setItemText(0, _translate("Form", "文本"))
        self.comboBox.setItemText(1, _translate("Form", "连接"))
        self.comboBox.setItemText(2, _translate("Form", "数组"))
        self.comboBox.setItemText(3, _translate("Form", "数组转文本"))
        self.comboBox.setItemText(4, _translate("Form", "文本拼接"))
        self.comboBox.setItemText(5, _translate("Form", "文本截取"))
        self.comboBox.setItemText(6, _translate("Form", "数组截取"))
        self.comboBox.setItemText(7, _translate("Form", "二值转换"))
        self.comboBox.setItemText(8, _translate("Form", "二值逆转换"))
        self.saveConf.setText(_translate("Form", "保存配置"))
        self.nextPage.setText(_translate("Form", "下一页"))
        self.lineEdit_3.setText(_translate("Form", "xpath"))
        self.comboBox_2.setItemText(0, _translate("Form", "连接"))
        self.comboBox_2.setItemText(1, _translate("Form", "文本拼接"))
        self.comboBox_2.setItemText(2, _translate("Form", "文本截取"))
