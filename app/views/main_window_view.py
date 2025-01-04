from core.views import PyQtierMainWindowView


class MainWindowView(PyQtierMainWindowView):
    def add_behaviour(self):
        self.ui.bt1.clicked.connect(self.get_callback('custom_widget'))
        self.ui.actionSettings.triggered.connect(self.get_callback('settings_widget'))
