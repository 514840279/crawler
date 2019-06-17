# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainContentSub.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(939, 421)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_3.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 0, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 0, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 0, 2, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setMinimumSize(QtCore.QSize(60, 0))
        self.pushButton_3.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 0, 3, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setMinimumSize(QtCore.QSize(60, 0))
        self.pushButton_4.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 0, 4, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 5)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 4)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lineEdit_3.setText(_translate("Dialog", "数据项名称"))
        self.lineEdit_4.setText(_translate("Dialog", "规则"))
        self.comboBox.setItemText(0, _translate("Dialog", "文字"))
        self.comboBox.setItemText(1, _translate("Dialog", "连接"))
        self.comboBox.setItemText(2, _translate("Dialog", "图片"))
        self.comboBox.setItemText(3, _translate("Dialog", "网页"))
        self.comboBox.setItemText(4, _translate("Dialog", "列表"))
        self.pushButton_3.setText(_translate("Dialog", "测试"))
        self.pushButton_4.setText(_translate("Dialog", "添加"))

