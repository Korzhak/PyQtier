from core.views import AbstractSettingsView, QtWidgets


class SettingsView(AbstractSettingsView):
    def __init__(self, widget: QtWidgets.QWidget):
        super(SettingsView, self).__init__(widget)
