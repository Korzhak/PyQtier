from core.views import AbstractSettingsView, QtWidgets
from core.widgets import WidgetRegistry


@WidgetRegistry.register("custom_widget")
class CustomWidget(AbstractSettingsView):
    def __init__(self, widget: QtWidgets.QWidget = None):
        if widget is None:
            widget = QtWidgets.QWidget()
        super(CustomWidget, self).__init__(widget)
