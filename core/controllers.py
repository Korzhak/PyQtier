# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtWidgets


class AbstractController:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = QtWidgets.QMainWindow()

    def show_ui(self):
        self.main_window.show()
        sys.exit(self.app.exec_())
