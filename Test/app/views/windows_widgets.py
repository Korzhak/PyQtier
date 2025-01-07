from app.models.settings import SettingsModel
from pyqtier.registry import PyQtierWidgetRegistry
from app.templates import Ui_SimpleView
from pyqtier.views import PyQtierSimpleView


@PyQtierWidgetRegistry.register("settings_widget", Ui_SimpleView, SettingsModel)
class SettingsWidget(PyQtierSimpleView):
    ...
