# -*- coding: utf-8 -*-

import types

from PyQt5 import QtWidgets

from templates.main_window_interface import Ui_MainWindow
from templates.settings_interface import Ui_Settings


class AbstractSettingsView(Ui_Settings):
    def __init__(self, widget: QtWidgets.QWidget):
        super(AbstractSettingsView, self).__init__()
        self.widget = widget
        self.setupUi(widget)

        self.__is_opened = False

        self.add_behaviour()

    def add_behaviour(self):
        """
        Add callbacks
        :return: None
        """
        # START YOUR CODE
        ...
        # END YOUR CODE

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
    def __init__(self, main_window_widget, settings, settings_view):
        super(AbstractMainWindowView, self).__init__()

        self.main_window_widget = main_window_widget
        self.settings = settings

        self.settings_widget = QtWidgets.QWidget()
        self.settings_window = settings_view(self.settings_widget)

        # Змінюємо метод closeEvent для вікна
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
        self.actionSettings.triggered.connect(self.show_settings_window)
        self.actionQuit.triggered.connect(self.quit)
        # START YOUR CODE
        ...
        # END YOUR CODE

    def show_settings_window(self):
        self.settings_window.open()

    def quit(self, window, event):
        """
        Callback for behaviour when window is closing
        return: ...
        """
        if self.settings_window.is_opened:
            self.settings_window.quit()
        event.accept()
