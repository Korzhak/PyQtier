# -*- coding: utf-8 -*-
from app.models import SettingsModel
from app.views import MainWindowView
from core import PyQtierWindowsManager
from core.templates.main_window_interface import Ui_MainWindow


class WindowsManager(PyQtierWindowsManager):
    def __init__(self):
        super().__init__()
        self.settings_window = None
        self.custom_window = None

    def setup_manager(self):
        self.setup_main_window(Ui_MainWindow, MainWindowView, SettingsModel)

        # Creating windows widgets
        self.custom_window = self.widget_registry.get_initialized_widget('custom_widget')
        self.settings_window = self.widget_registry.get_initialized_widget('settings_widget')

        # Registering callback in windows
        self.main_window.register_callback("custom_widget", self.custom_window.open)
        self.main_window.register_callback("settings_widget", self.settings_window.open)

        # Adding behaviours to widgets (must be the last section)
        self.main_window.add_behaviour()
