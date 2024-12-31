from core.views import AbstractMainWindowView


class MainWindowView(AbstractMainWindowView):
    def __init__(self, main_window_widget, settings):
        super(MainWindowView, self).__init__(main_window_widget, settings)
        self.add_behaviour()

    def add_behaviour(self):
        super(MainWindowView, self).add_behaviour()
        self.bt1.clicked.connect(self.bt1_clicked)

    def bt1_clicked(self):
        ...
