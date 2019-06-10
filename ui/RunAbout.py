from PyQt5.QtWidgets import QWidget

from ui.about import Ui_Form


class RunAbout(QWidget, Ui_Form):
    def __init__(self):
        super(RunAbout, self).__init__()
        self.setupUi(self)
