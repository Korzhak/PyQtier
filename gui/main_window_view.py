# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

from gui.settings_view import SettingsView
from gui.ui.main_window_interface import Ui_MainWindow


class MainWindowView(Ui_MainWindow):
    def __init__(self, main_window_widget, settings):
        super(MainWindowView, self).__init__()

        self.__main_window_widget = main_window_widget
        self.__settings = settings

        self.__settings_widget = QtWidgets.QWidget()
        self.__settings_window = SettingsView(self.__settings_widget)
        # YOUR CODE START
        ...
        # YOUR CODE END

        self.setupUi(self.__main_window_widget)
        self.__add_behaviour()

    def __add_behaviour(self):
        """
        Add callbacks
        :return: None
        """
        self.actionSettings.triggered.connect(self.__show_settings_window)
        self.actionQuit.triggered.connect(self.quit)
        # START YOUR CODE
        ...
        # END YOUR CODE

    def __show_settings_window(self):
        self.__settings_window.open()

    def quit(self):
        """
        Callback for behaviour when window is closing
        return: ...
        """
        # START YOUR CODE
        ...
        # END YOUR CODE
        if self.__settings_window.is_opened:
            return
        QtWidgets.qApp.quit()
