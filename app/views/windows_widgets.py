from app.models.settings import SettingsModel
from core.registry import WidgetRegistry
from core.templates.custom import Ui_Form
from core.templates.simple_interface import Ui_SimpleView
from core.views import AbstractSimpleView


@WidgetRegistry.register("settings_widget", Ui_SimpleView, SettingsModel)
class SettingsWidget(AbstractSimpleView):
    def __init__(self):
        super().__init__()


@WidgetRegistry.register("custom_widget", Ui_Form, SettingsModel)
class CustomWidget(AbstractSimpleView):
    def __init__(self):
        super().__init__()
