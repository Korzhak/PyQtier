from core.models import SettingsModel
from core.views import AbstractMainWindowView

from views.settings_view import SettingsView


class MainWindowView(AbstractMainWindowView):
    def __init__(self, main_window_widget, settings: SettingsModel):
        super(MainWindowView, self).__init__(main_window_widget, settings, SettingsView)
        self.add_behaviour()

    def add_widgets(self):
        super().add_widgets()
        self.widget_manager.add_window_widget("custom_widget")
        # self.widget_manager.add_widget("control_panel", area="dock")

    def add_behaviour(self):
        super(MainWindowView, self).add_behaviour()
        self.actionSettings.triggered.connect(lambda: self.widget_manager.show_widget_window("custom_widget"))
