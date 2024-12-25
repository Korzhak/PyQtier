from core.views import AbstractSimpleView, QtWidgets
from core.widgets import WidgetRegistry
from templates.custom import Ui_Form


@WidgetRegistry.register("custom_widget", Ui_Form, QtWidgets)
class CustomWidget(AbstractSimpleView):
    def __str__(self):
        print("custom widget class")
