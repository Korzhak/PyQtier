# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets

from core.registry import PyQtierWidgetRegistry


class PyQtierWindowsManager:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window_widget = QtWidgets.QMainWindow()
        self.main_window = None

        self.widget_registry = PyQtierWidgetRegistry()
        self.widget_registry.create_registered_widgets()

        self.setup_manager()

    def setup_manager(self):
        ...

    def setup_main_window(self, main_window_view, settings):
        """
        Setup main
        """
        self.main_window = main_window_view(self.main_window_widget, settings)

    def show_ui(self):
        self.main_window_widget.show()
        sys.exit(self.app.exec_())
