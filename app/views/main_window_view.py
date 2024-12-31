from core.views import AbstractMainWindowView


class MainWindowView(AbstractMainWindowView):

    def __init__(self, main_window_widget, settings):
        super(MainWindowView, self).__init__(main_window_widget, settings)

    def add_behaviour(self):
        super(MainWindowView, self).add_behaviour()
        self.bt1.clicked.connect(self.get_callback('custom_widget'))
        self.actionSettings.triggered.connect(self.get_callback('settings_widget'))
