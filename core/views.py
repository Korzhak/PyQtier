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

    def setup_view(self, ui=None, settings=None, widget=None, settings_id: str = "", ):
        self.widget = widget if widget else QtWidgets.QWidget()

        self.settings_id = settings_id if settings_id else self.__class__.__name__

        self.ui = ui()
        self.settings = settings(self.settings_id)
        self.ui.setupUi(self.widget)
        self.add_behaviour()

    def load_config(self):
        # Size and position for main window
        w, h = self.settings.window_size
        x, y = self.settings.window_position
        if w and h:
            self.ui.resize(w, h)
        if x and y:
            self.ui.move(x, y)

    def save_settings(self):
        # Size and position for main window
        self.settings.set_window_size(self.ui.size().width(),
                                      self.ui.size().height())

        self.settings.set_window_position(self.ui.pos().x(),
                                          self.ui.pos().y())

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

    def quit(self):
        """
        Close the settings window
        :return: None
        """
        self.save_settings()
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
    _callbacks = {}

    def __init__(self, main_window_widget, settings):
        super(AbstractMainWindowView, self).__init__()

        self.main_window_widget = main_window_widget
        self.settings = settings()

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
        w, h = self.settings.window_size
        x, y = self.settings.window_position
        if w and h:
            self.main_window_widget.resize(w, h)
        if x and y:
            self.main_window_widget.move(x, y)

    def save_settings(self):
        # Size and position for main window
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
