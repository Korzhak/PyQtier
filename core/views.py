# -*- coding: utf-8 -*-

import types

from PyQt5 import QtWidgets

from core.templates.main_window_interface import Ui_MainWindow


class AbstractSimpleView:
    def __init__(self):
        self.settings = None
        self.settings_id = None
        self.ui = None
        self.widget = None
        self.__is_opened = False

    def setup_view(self, ui=None, settings=None, widget=None, settings_id: str = ""):
        self.widget = widget if widget else QtWidgets.QWidget()

        self.settings_id = settings_id if settings_id else self.__class__.__name__

        self.ui = ui()
        self.widget.closeEvent = types.MethodType(self.quit, self.widget)
        self.settings = settings(self.settings_id)
        self.ui.setupUi(self.widget)
        self.add_behaviour()

    def load_config(self):
        # Size and position for main window
        if self.settings.is_maximized:
            self.widget.showMaximized()
        else:
            w, h = self.settings.window_size
            x, y = self.settings.window_position
            if w and h:
                self.widget.resize(w, h)
            if x and y:
                self.widget.move(x, y)

    def save_settings(self):
        """

        :return:
        """
        is_maximized = self.widget.isMaximized()
        self.settings.set_maximized(is_maximized)
        if not is_maximized:
            self.settings.set_window_size(self.widget.size().width(),
                                          self.widget.size().height())

            self.settings.set_window_position(self.widget.pos().x(),
                                              self.widget.pos().y())

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
        self.load_config()
        self.widget.show()
        self.__is_opened = True

    def quit(self, window, event):
        """
        Close the settings window
        :return: None
        """
        self.save_settings()
        self.widget.close()
        self.__is_opened = False
        event.accept()

    @property
    def is_opened(self):
        """
        Check if the settings window is opened
        :return: True if the settings window is opened else false
        """
        return self.__is_opened


class AbstractMainWindowView(Ui_MainWindow):
    _callbacks = {}

    def __init__(self, main_window_widget, settings):
        super(AbstractMainWindowView, self).__init__()

        self.main_window_widget = main_window_widget
        self.settings = settings(settings_id="main")

        # Change closeEvent method to custom
        self.main_window_widget.closeEvent = types.MethodType(self.quit, self.main_window_widget)

        self.setupUi(self.main_window_widget)
        self.load_config()

    def register_callback(self, callback_id: str, callback_func: callable):
        self._callbacks[callback_id] = callback_func

    def get_callback(self, callback_id: str):
        return self._callbacks[callback_id]

    def remove_callback(self, callback_id: str):
        ...

    def load_config(self):
        # Size and position for main window
        if self.settings.is_maximized:
            self.main_window_widget.showMaximized()
        else:
            w, h = self.settings.window_size
            x, y = self.settings.window_position
            if w and h:
                self.main_window_widget.resize(w, h)
            if x and y:
                self.main_window_widget.move(x, y)

    def save_settings(self):
        # Size and position for main window
        is_maximized = self.main_window_widget.isMaximized()
        self.settings.set_maximized(is_maximized)
        if not is_maximized:
            self.settings.set_window_size(self.main_window_widget.size().width(),
                                          self.main_window_widget.size().height())

            self.settings.set_window_position(self.main_window_widget.pos().x(),
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
        self.save_settings()
        event.accept()
