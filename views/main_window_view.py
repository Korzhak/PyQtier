from core.models import SettingsModel
from core.views import AbstractMainWindowView

from views.settings_view import SettingsView


class MainWindowView(AbstractMainWindowView):
    def __init__(self, main_window_widget, settings: SettingsModel):
        super(MainWindowView, self).__init__(main_window_widget, settings, SettingsView)

    def add_behaviour(self):
        super(MainWindowView, self).add_behaviour()
