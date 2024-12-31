from core.views import AbstractSimpleView, QtWidgets
from core.widgets import WidgetRegistry
from app.templates.custom import Ui_Form


@WidgetRegistry.register("custom_widget")
class CustomWidget(AbstractSimpleView):
    def __str__(self):
        print("custom widget class")
