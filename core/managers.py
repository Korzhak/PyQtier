# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets

from core.widgets.registry import WidgetRegistry


class PyQtierWindowsManager:
    def __init__(self):
        self.widget_registry = WidgetRegistry()
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window_widget = QtWidgets.QMainWindow()
        self.main_window = None
        self.create_widgets()
        self.setup_manager()

    def setup_manager(self):
        ...

    def create_widgets(self):
        ...

    def show_ui(self):
        self.main_window_widget.show()
        sys.exit(self.app.exec_())
