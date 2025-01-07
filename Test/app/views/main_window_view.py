from pyqtier.views import PyQtierMainWindowView


class MainWindowView(PyQtierMainWindowView):
    def add_behaviour(self):
        self.ui.actionSettings.triggered.connect(self.get_callback('settings_widget'))
