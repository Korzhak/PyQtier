# -*- coding: utf-8 -*-
from app.models import SettingsModel
from app.views import MainWindowView
from core import PyQtierWindowsManager


class WindowsManager(PyQtierWindowsManager):
    def setup_manager(self):
        self.setup_main_window(MainWindowView, SettingsModel)

        self.custom_window = self.widget_registry.get_initialized_widget('custom_widget')
        self.settings_window = self.widget_registry.get_initialized_widget('settings_widget')
        #
        self.main_window.register_callback("custom_widget", self.custom_window.open)
        self.main_window.register_callback("settings_widget", self.settings_window.open)

        self.main_window.add_behaviour()
