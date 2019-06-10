from PyQt5.QtWidgets import QWidget

from ui.mainContext import Ui_Form


class RunMainContext(QWidget, Ui_Form):
    def __init__(self):
        super(RunMainContext, self).__init__()
        self.setupUi(self)
