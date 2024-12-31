from core.registry import WidgetRegistry
from core.templates.simple_interface import Ui_SimpleView
from core.views import AbstractSimpleView


@WidgetRegistry.register("custom_widget", Ui_SimpleView)
class CustomWidget(AbstractSimpleView):
    ...
