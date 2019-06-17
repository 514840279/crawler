# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from ui.mainContentSub import Ui_Dialog
from common.HtmlSource import HtmlSource


class RunMainContextSub(QWidget, Ui_Dialog):
    def __init__(self):
        super(RunMainContextSub, self).__init__()
        self.setupUi(self)
