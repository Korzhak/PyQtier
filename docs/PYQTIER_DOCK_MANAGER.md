# PyQtierDockManager

Менеджер док-віджетів на базі PyQtAds для PyQtier фреймворку.

## Встановлення

```bash
pip install PyQtAds
```

## Базове використання

```python
from pyqtier.widgets import PyQtierMainWindow, PyQtierDockManager
from PyQtAds import ads


class MainWindow(PyQtierMainWindow):
    def setup_view(self):
        # Створення
        self.dock_manager = PyQtierDockManager(self.view.main_frame)
        self.dock_manager.setup()
        self.view.main_layout.addWidget(self.dock_manager.get_widget())

        # Додавання доків
        self.dock_manager.add("Графік", self.plot_widget, ads.CenterDockWidgetArea)
        self.dock_manager.add("Панель", self.control_widget, ads.LeftDockWidgetArea)

        # Меню "Вид" (опціонально)
        self.view_menu = self.view.menubar.addMenu("Вид")
        self.dock_manager.create_view_menu(self.view_menu)

    def _save_additional_state(self):
        self.settings.setValue("docks", self.dock_manager.save_state())

    def _restore_additional_state(self):
        if state := self.settings.value("docks"):
            self.dock_manager.restore_state(state)
```

## Області розміщення

```python
ads.LeftDockWidgetArea    # Ліва панель
ads.RightDockWidgetArea   # Права панель
ads.TopDockWidgetArea     # Верхня панель
ads.BottomDockWidgetArea  # Нижня панель
ads.CenterDockWidgetArea  # Центр
```

## Меню "Вид"

**Немає свого меню:**
```python
self.view_menu = self.view.menubar.addMenu("Вид")
self.dock_manager.create_view_menu(self.view_menu)
```

**Є своє меню з UI файлу:**
```python
self.view.menuView.addSeparator()
self.dock_manager.create_view_menu(self.view.menuView)
```

## Методи

| Метод                     | Опис |
|---------------------------|------|
| `setup(**flags)`          | Ініціалізація |
| `get_widget()`            | Qt-віджет для layout |
| `add(name, widget, area)` | Додати док |
| `get(name)`               | Отримати док за назвою |
| `is_open(name)`           | Чи відкритий |
| `show(name)`              | Показати |
| `hide(name)`              | Сховати |
| `toggle(name, show)`      | Перемкнути |
| `show_all()`              | Показати всі |
| `hide_all()`              | Сховати всі |
| `get_names()`             | Список назв |
| `save_state()`            | Зберегти стан віджетів |
| `restore_state(json)`     | Відновити стан віджетів |
| `set_style(style)`        | Змінити тему |
| `create_view_menu(menu)`  | Додати пункти в меню |

## Теми

```python
# При створенні
self.dock_manager = PyQtierDockManager(parent, style="dark")  # або "light"

# Пізніше
self.dock_manager.set_style("light")

# Свій CSS
self.dock_manager.set_style("ads--CDockAreaTitleBar { background: red; }")
```

## Оптимізація оновлення

Оновлюй тільки відкриті доки:

```python
def obtain_data(self, data):
    if self.dock_manager.is_open("Графік"):
        self.plot_widget.update(data)
```
