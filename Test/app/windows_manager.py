# -*- coding: utf-8 -*-
from pyqtier import PyQtierWindowsManager

from app.models import SettingsModel
from app.templates import Ui_MainWindow
from app.views import MainWindowView


class WindowsManager(PyQtierWindowsManager):
    def __init__(self):
        super().__init__()
        self.settings_window = None

    def setup_manager(self):
        self.setup_main_window(Ui_MainWindow, MainWindowView, SettingsModel)

        # Creating windows widgets
        self.settings_window = self.widget_registry.get_initialized_widget('settings_widget')

        self.main_window.register_callback('settings_widget', self.settings_window.open)

        # Adding behaviours to widgets (must be the last section)
        self.main_window.add_behaviour()


    