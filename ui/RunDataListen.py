from PyQt5.QtWidgets import QWidget

from ui.dataListen import Ui_Form


class RunDataListen(QWidget, Ui_Form):
    def __init__(self):
        super(RunDataListen, self).__init__()
        self.setupUi(self)
