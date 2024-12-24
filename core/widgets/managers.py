from .registry import WidgetRegistry
from .widgets import WidgetWindow


class WidgetManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.widgets = {}
        self.windows = {}  # Зберігаємо посилання на відкриті вікна

    def add_window_widget(self, widget_id: str):
        """
        Додавання віджета
        :param widget_id: ідентифікатор віджета
        :param area: місце розташування (central, dock, window)
        """
        widget = WidgetRegistry.create_widget(widget_id)
        self.windows[widget_id] = widget

    def show_widget_window(self, widget_id: str):
        """Показати віджет в окремому вікні"""
        print(widget_id)
        if widget_id not in self.windows:
            self.add_window_widget(widget_id)
        else:
            widget = self.widgets[widget_id]
            # Якщо віджет вже відображається, просто показуємо вікно
            if widget_id in self.windows:
                self.windows[widget_id].open()
                self.windows[widget_id].activateWindow()
            else:
                # Створюємо нове вікно
                window = WidgetWindow(widget, self.main_window)
                self.windows[widget_id] = window
                window.open()

    def close_widget_window(self, widget_id: str):
        """Закрити окреме вікно віджета"""
        if widget_id in self.windows:
            self.windows[widget_id].quit()
            del self.windows[widget_id]
