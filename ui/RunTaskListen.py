from PyQt5.QtWidgets import QWidget

from ui.taskListen import  Ui_Form


class RunTaskListen(QWidget, Ui_Form):
    def __init__(self):
        super(RunTaskListen, self).__init__()
        self.setupUi(self)
