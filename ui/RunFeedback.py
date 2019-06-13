from PyQt5.QtWidgets import QWidget

from ui.feedback import Ui_Form


class RunFeedback(QWidget, Ui_Form):
    def __init__(self):
        super(RunFeedback, self).__init__()
        self.setupUi(self)
