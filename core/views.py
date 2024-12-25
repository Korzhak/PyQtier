# -*- coding: utf-8 -*-

import types

from PyQt5 import QtWidgets

from templates.main_window_interface import Ui_MainWindow
from templates.simple_interface import Ui_SimpleView
from .widgets import WindowWidgetManager


class AbstractSimpleView:
    def __init__(self, ui=None, widget=None):
        if not widget:
            self.widget = widget
        else:
            self.widget = QtWidgets.QWidget()
        if not ui:
            self.ui = ui
        else:
            self.ui = Ui_SimpleView()
        self.ui.setupUi(self.widget)

        self.__is_opened = False

        self.add_behaviour()

    def add_behaviour(self):
        """
        Add callbacks
        :return: None
        """

    def open(self):
        """
        Open the settings window
        :return: None
        """
        self.widget.show()
        self.__is_opened = True

    def quit(self):
        """
        Close the settings window
        :return: None
        """
        self.widget.close()
        self.__is_opened = False

    @property
    def is_opened(self):
        """
        Check if the settings window is opened
        :return: True if the settings window is opened else false
        """
        return self.__is_opened


class AbstractMainWindowView(Ui_MainWindow):
    def __init__(self, main_window_widget, settings):
        super(AbstractMainWindowView, self).__init__()

        self.main_window_widget = main_window_widget
        self.settings = settings

        self.widget_manager = WindowWidgetManager(self)

        # Change closeEvent method to custom
        self.main_window_widget.closeEvent = types.MethodType(self.quit, self.main_window_widget)

        self.setupUi(self.main_window_widget)
        self.add_behaviour()

    def load_config(self):
        # Size and position for main window
        w, h = self.settings.main_window_size
        x, y = self.settings.main_window_position
        self.main_window_widget.resize(w, h)
        self.main_window_widget.move(x, y)

    def save_settings(self):
        # Size and position for main window
        self.settings.set_main_window_size(self.main_window_widget.size().width(),
                                           self.main_window_widget.size().height())

        self.settings.set_main_window_position(self.main_window_widget.pos().x(),
                                               self.main_window_widget.pos().y())

    def add_behaviour(self):
        """
        Add callbacks
        :return: None
        """
        self.actionQuit.triggered.connect(self.quit)

    def quit(self, window, event):
        """
        Callback for behaviour when window is closing
        return: ...
        """
        event.accept()
