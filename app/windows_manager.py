# -*- coding: utf-8 -*-
from app.models import SettingsModel
from app.views import MainWindowView
from core import PyQtierWindowsManager
from core.templates.simple_interface import Ui_SimpleView


class WindowsManager(PyQtierWindowsManager):
    def setup_manager(self):
        self.setup_main_window(MainWindowView, SettingsModel)
