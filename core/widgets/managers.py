from .registry import WidgetRegistry


class WidgetManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.widgets = {}

    def add_widget(self, widget_id: str):
        ...

    def remove_widget(self, widget_id: str):
        ...

    def show_widget(self, widget_id: str):
        ...

    def close_widget(self, widget_id: str):
        ...


class WindowWidgetManager(WidgetManager):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.windows = {}
        self.opened_windows = {}  # Зберігаємо посилання на відкриті вікна

    def add_widget(self, widget_id: str):
        """
        Додавання віджета
        :param widget_id: ідентифікатор віджета
        """
        widget = WidgetRegistry.create_widget(widget_id)
        self.windows[widget_id] = widget

    def show_widget(self, widget_id: str):
        """
        Show widget in separate window
        :param widget_id: name of widget
        :return: None
        """
        if widget_id not in self.windows:
            raise KeyError(f"Widget {widget_id} is not registered")
        else:
            widget = self.windows[widget_id]
            # Якщо віджет вже відображається, просто показуємо вікно
            if widget_id in self.opened_windows:
                self.opened_windows[widget_id].open()
            else:
                # Створюємо нове вікно
                self.opened_windows[widget_id] = widget
                widget.open()

        print(self.opened_windows)

    def close_widget(self, widget_id: str):
        """Закрити окреме вікно віджета"""
        if widget_id in self.opened_windows:
            self.opened_windows[widget_id].quit()
            del self.opened_windows[widget_id]
