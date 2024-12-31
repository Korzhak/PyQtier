from typing import Callable, Any


class WidgetRegistry:
    _widgets = {}

    @classmethod
    def register(cls, widget_id: str) -> Callable[[Any], Any]:
        def decorator(widget_class):
            cls._widgets[widget_id] = widget_class
            return widget_class

        return decorator

    @classmethod
    def create_widget(cls, widget_id: str, template=None, widget_class: Callable[[Any], Any] = None) -> Callable[
        [Any], Any]:
        if widget_id not in cls._widgets:
            raise ValueError(f"Widget {widget_id} not found")
        return cls._widgets[widget_id](template, widget_class)
