class WidgetRegistry:
    _widgets = {}

    @classmethod
    def register(cls, widget_id: str):
        def decorator(widget_class):
            cls._widgets[widget_id] = widget_class
            return widget_class
        return decorator

    @classmethod
    def create_widget(cls, widget_id: str):
        if widget_id not in cls._widgets:
            raise ValueError(f"Widget {widget_id} not found")
        return cls._widgets[widget_id]()
