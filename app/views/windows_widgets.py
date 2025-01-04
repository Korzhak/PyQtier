from app.models.settings import SettingsModel
from core.registry import PyQtierWidgetRegistry
from core.templates.custom import Ui_Form
from core.templates.simple_interface import Ui_SimpleView
from core.views import PyQtierSimpleView


@PyQtierWidgetRegistry.register("settings_widget", Ui_SimpleView, SettingsModel)
class SettingsWidget(PyQtierSimpleView):
    def __init__(self):
        super().__init__()
        self.counter = 0


@PyQtierWidgetRegistry.register("custom_widget", Ui_Form, SettingsModel)
class CustomWidget(PyQtierSimpleView):
    def __init__(self):
        super().__init__()
        self.counter = 0

    def add_behaviour(self):
        self.ui.pushButton.clicked.connect(self.update)

    def update(self):
        self.counter += 1
        print(self.counter)
