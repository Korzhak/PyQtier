from typing import Callable, Any


class WidgetRegistry:
    _widgets = {}
    _uis = {}
    _base_widgets = {}

    @classmethod
    def register(cls, widget_id: str, ui_class: type = None, base_widget=None) -> Callable[[Any], Any]:
        def decorator(widget_class):
            cls._widgets[widget_id] = widget_class
            cls._uis[widget_id] = ui_class
            cls._uis[widget_id] = ui_class
            cls._base_widgets[widget_id] = base_widget
            return widget_class

        return decorator

    @classmethod
    def create_widget(cls, widget_id: str):
        if widget_id not in cls._widgets:
            raise ValueError(f"Widget {widget_id} not found")
        return cls._widgets[widget_id](cls._uis[widget_id], cls._base_widgets[widget_id])
