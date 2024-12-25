from core.models import SettingsModel
from core.views import AbstractMainWindowView


class MainWindowView(AbstractMainWindowView):
    def __init__(self, main_window_widget, settings: SettingsModel):
        super(MainWindowView, self).__init__(main_window_widget, settings)
        self.add_behaviour()
        self.add_widgets()

    def add_widgets(self):
        super().add_widgets()
        self.widget_manager.add_widget("custom_widget")

    def add_behaviour(self):
        super(MainWindowView, self).add_behaviour()
        self.actionSettings.triggered.connect(lambda: self.widget_manager.show_widget_window("custom_widget"))
        self.bt1.clicked.connect(self.bt1_clicked)

    def bt1_clicked(self):
        self.widget_manager.show_widget('custom_widget')