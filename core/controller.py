# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtWidgets

from core.settings import Settings
from gui.main_window_view import MainWindowView


class Controller:
    def __init__(self):
        self.settings = Settings()

        self.__app = QtWidgets.QApplication(sys.argv)
        self.__main_window = QtWidgets.QMainWindow()

        self.__view = MainWindowView(self.__main_window, self.settings)

    def show_ui(self):
        self.__main_window.show()
        sys.exit(self.__app.exec_())
