from core.views import AbstractSimpleView
from core.widgets import WidgetRegistry


@WidgetRegistry.register("custom_widget")
class CustomWidget(AbstractSimpleView):
    ...
