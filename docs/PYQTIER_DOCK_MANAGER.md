# PyQtierDockManager

Менеджер док-віджетів на базі PyQtAds для PyQtier фреймворку. Напряму успадковує `ads.CDockManager`.

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
        # Створення (автоматично додається в layout батьківського віджета)
        self.dock_manager = PyQtierDockManager(self.view.main_frame, style="dark")

        # Додавання доків
        self.dock_manager.add("Графік", self.plot_widget, ads.CenterDockWidgetArea)
        self.dock_manager.add("Панель", self.control_widget, ads.LeftDockWidgetArea)

        # Меню "Вид" (опціонально)
        self.view_menu = self.view.menubar.addMenu("Вид")
        self.dock_manager.create_view_menu(self.view_menu)

        # Реакція на зміну стану доків (опціонально)
        self.dock_manager.state_changed.connect(self.on_dock_state_changed)

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

**Немає свого меню "Вид":**
```python
self.view_menu = self.view.menubar.addMenu("Вид")
self.dock_manager.create_view_menu(self.view_menu)
```

**Є своє меню "Вид" з UI файлу:**
```python
self.dock_manager.create_view_menu(self.view.menuView)
```

## Конструктор

```python
PyQtierDockManager(parent, style="dark", **flags)
```

- `parent` - батьківський віджет
- `style` - тема: `"dark"`, `"light"` або власний CSS
- `**flags` - перевизначення конфігурації (див. нижче)

**Автододавання в layout:** Якщо `parent` вже має layout, dock manager автоматично додається в нього. Це працює з `PyQtierMainWindow`, де `main_frame` має layout.

```python
# PyQtierMainWindow - достатньо (layout є)
self.dock_manager = PyQtierDockManager(self.view.main_frame)

# Свій віджет без layout - потрібно вручну
self.dock_manager = PyQtierDockManager(my_widget)
my_layout.addWidget(self.dock_manager)
```

### Конфігурація за замовчуванням

```python
CONFIG_DEFAULTS = {
    'OpaqueSplitterResize': True,
    'XmlCompressionEnabled': False,
    'DockAreaHasTabsMenuButton': False,
    'DockAreaHasUndockButton': False,
    'HideSingleCentralWidgetTitleBar': True,
    'MiddleMouseButtonClosesTab': True,
}
```

Перевизначення:
```python
dock_manager = PyQtierDockManager(parent, DockAreaHasUndockButton=True)
```

## Методи

| Метод                         | Опис |
|-------------------------------|------|
| `add(name, widget, area, into)` | Додати док |
| `get(name)`                   | Отримати док за назвою |
| `is_open(name)`               | Чи відкритий |
| `show(name)`                  | Показати |
| `hide(name)`                  | Сховати |
| `toggle(name, show)`          | Перемкнути |
| `show_all()`                  | Показати всі |
| `hide_all()`                  | Сховати всі |
| `all_docks()`                 | Словник всіх доків `{name: CDockWidget}` |
| `get_names()`                 | Список назв всіх доків |
| `open_names()`                | Список назв відкритих доків |
| `closed_names()`              | Список назв закритих доків |
| `save_state()`                | Зберегти стан (JSON) |
| `restore_state(json)`         | Відновити стан |
| `set_style(style)`            | Змінити тему |
| `create_view_menu(menu)`      | Додати пункти в меню |


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
