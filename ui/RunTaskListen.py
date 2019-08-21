from PyQt5.QtWidgets import QWidget

from ui.taskListen import  Ui_Form
from common.ResultData import SysCrawlerTaskInfo
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout,QWidget,QPushButton,QTableWidgetItem, QLabel, QVBoxLayout
import datetime
import requests,time


class RunTaskListen(QWidget, Ui_Form):
    def __init__(self):
        super(RunTaskListen, self).__init__()
        self.setupUi(self)
        self.showTables()

    def showTables(self):

        self.tableWidget.setVisible(True)
        sysCrawlerTaskInfo = SysCrawlerTaskInfo()
        taskListData = sysCrawlerTaskInfo.findAll()
        if taskListData != False:
            #title = list(taskListData[0].keys())
            title = ['操作','图标','task_name',
                     #'url',
                     'url_type','url_name','discription',
                     'charset','request_data','request_type',
                     'excute_batch','excute_flag',
                     #'create_time','create_user',
                     'update_time','update_user'
                     #,'start_time','home_statue','dict_conf','list_conf','detail_conf'
                     ]

            # 设置数据层次结构，4行4列
            self.tableWidget.setRowCount(99)  # 行下标最大值
            self.tableWidget.setColumnCount(len(title))  # 列

            # 设置水平方向四个头标签文本内容
            self.tableWidget.setHorizontalHeaderLabels(title)

            for row in range(len(taskListData)):
                if taskListData[row]['delete_flag'] is not 1:
                    button = self.buttonForDeleteTrue(id=taskListData[row]['uuid'])
                    # 设置每个位置的按钮
                    self.tableWidget.setCellWidget(row, 0, button)
                else:
                    button = self.buttonForDeleteFalse(id=taskListData[row]['uuid'])
                    # 设置每个位置的按钮
                    self.tableWidget.setCellWidget(row, 0, button)

                if taskListData[row]['web_icon'] is not None:
                    img = self.showImg(url=taskListData[row]['web_icon'] )
                    # 设置每个位置的按钮
                    self.tableWidget.setCellWidget(row, 1, img)
                else:
                    # 设置每个位置的按钮
                    self.tableWidget.setCellWidget(row, 1, None)

                for column in range(len(title)-2):
                    print(taskListData[row])
                    data = taskListData[row][title[column+2]]
                    if isinstance(data, datetime.datetime):
                        date = data.strftime("%Y-%m-%d %H:%M:%S")
                        item = QTableWidgetItem(date)
                        # 设置每个位置的文本值
                        self.tableWidget.setItem(row, column+2, item)
                    else:
                        item = QTableWidgetItem(data)
                        # 设置每个位置的文本值
                        self.tableWidget.setItem(row, column+2, item)
        del sysCrawlerTaskInfo


    # 列表内添加按钮
    def buttonForDeleteTrue(self, id):

        widget = QWidget()
        # 修改
        updateBtn = QPushButton('已启用')
        updateBtn.setStyleSheet(''' text-align : center;
                                          background-color : NavajoWhite;
                                          height : 30px;
                                          border-style: outset;
                                          font : 13px  ''')
        updateBtn.clicked.connect(lambda: self.updateDeleteFalse(id))

        hLayout = QHBoxLayout()
        hLayout.addWidget(updateBtn)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    def updateDeleteFalse(self,id):
        sysCrawlerTaskInfo = SysCrawlerTaskInfo()
        sysCrawlerTaskInfo.updateDelete(id,1)
        del sysCrawlerTaskInfo
        self.showTables()

    # 列表内添加按钮
    def buttonForDeleteFalse(self, id):
        widget = QWidget()

        # 删除
        deleteBtn = QPushButton('已废弃')
        deleteBtn.setStyleSheet(''' text-align : center;
                                    background-color : LightCoral;
                                    height : 30px;
                                    border-style: outset;
                                    font : 13px; ''')
        deleteBtn.clicked.connect(lambda: self.updateDeleteTrue(id))
        hLayout = QHBoxLayout()
        hLayout.addWidget(deleteBtn)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    def updateDeleteTrue(self,id):
        sysCrawlerTaskInfo = SysCrawlerTaskInfo()
        sysCrawlerTaskInfo.updateDelete(id,0)
        del sysCrawlerTaskInfo
        self.showTables()

    def showImg(self,url):
        req = requests.get(url)
        photo = QPixmap()

        photo.loadFromData(req.content)

        label = QLabel()
        label.setPixmap(photo)

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(label)

        widget.show()
        return widget