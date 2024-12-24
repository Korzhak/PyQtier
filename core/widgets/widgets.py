from PyQt5 import QtWidgets, uic


class BaseWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui_path = None
        self._settings = None
        self.setup()

    def setup(self):
        """Налаштування віджета"""
        if self._ui_path:
            self.load_ui()
        self.setup_signals()

    def load_ui(self):
        """Завантаження UI з .ui файлу"""
        if not self._ui_path:
            raise ValueError("UI path is not set")

        try:
            # Завантажуємо UI файл
            uic.loadUi(self._ui_path, self)
        except Exception as e:
            raise RuntimeError(f"Failed to load UI file {self._ui_path}: {str(e)}")

    def setup_signals(self):
        """Налаштування сигналів"""
        print('setup_signals')
        pass

    def save_state(self):
        """Збереження стану віджета"""
        pass

    def restore_state(self):
        """Відновлення стану віджета"""
        pass


class WidgetWindow(QtWidgets.QMainWindow):
    """Окреме вікно для віджета"""

    def __init__(self, widget, parent=None):
        super().__init__()
        print(widget)
        self.setWindowTitle(widget.windowTitle() or "Widget Window")
        self.setCentralWidget(widget)
        # Зберігаємо розмір і позицію вікна
        self.settings = widget._settings
        if self.settings:
            self.restore_geometry()

    def closeEvent(self, event):
        """Зберігаємо геометрію вікна перед закриттям"""
        if self.settings:
            self.save_geometry()
        event.accept()

    def save_geometry(self):
        """Зберігання позиції та розміру вікна"""
        geometry = {
            'size': (self.size().width(), self.size().height()),
            'pos': (self.pos().x(), self.pos().y())
        }
        self.settings.setValue(f"WindowGeometry/{self.windowTitle()}", geometry)

    def restore_geometry(self):
        """Відновлення позиції та розміру вікна"""
        geometry = self.settings.value(f"WindowGeometry/{self.windowTitle()}")
        if geometry:
            self.resize(*geometry['size'])
            self.move(*geometry['pos'])
