# -*- coding: utf-8 -*-
from core import PyQtierWindowsManager
from app.templates.custom import Ui_Form
from app.views.widgets import *


class WindowsManager(PyQtierWindowsManager):
    def setup_manager(self):
        super().setup_manager()
        self.main_window = self.widget_registry.create_widget("main_window_view", self.main_window_widget)

    def setup_main_window(self):
        ...

    def create_widgets(self):
        self.widget_registry.create_widget("main_window_view")
        self.widget_registry.create_widget("custom_widget", Ui_Form)
