from typing import Callable, Any


class WidgetRegistry:
    _widgets = {}
    _templates = {}
    _widgets_initialized = {}

    @classmethod
    def register(cls, widget_id: str, template) -> Callable[[Any], Any]:
        def decorator(widget_class):
            cls._widgets[widget_id] = widget_class
            cls._templates[widget_id] = template
            return widget_class

        return decorator

    @classmethod
    def create_registered_widgets(cls):
        for widget_id in cls._widgets:
            widget = cls._widgets[widget_id]()
            cls._widgets_initialized[widget_id] = widget
            return cls._widgets_initialized[widget_id].setup_view(cls._templates[widget_id])
