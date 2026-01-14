import json
from typing import Dict, List, Optional

from PyQt5.QtCore import QByteArray, QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget

try:
    from PyQtAds import ads
except ImportError:
    raise ImportError("PyQtAds is required. Install: pip install PyQtAds")


class PyQtierDockManager(QObject):
    state_changed = pyqtSignal()
    dock_closed = pyqtSignal(str)
    dock_opened = pyqtSignal(str)

    DARK_STYLE = """
        /* Кнопка закриття на вкладці (приховано) */
        ads--CDockWidgetTab > QPushButton { max-width: 0; max-height: 0; padding: 0; margin: 0; border: none; }

        /* Заголовок області доків (верхня панель з вкладками) */
        ads--CDockAreaTitleBar { background: rgb(40,40,40); min-height: 15px; max-height: 15px; }

        /* Кнопки в заголовку (закрити, меню) */
        ads--CDockAreaTitleBar QAbstractButton { background: rgb(40,40,40); border: none; }

        /* Текст неактивної вкладки */
        ads--CDockWidgetTab QLabel { background: rgb(40,40,40); color: rgb(100,100,100); }

        /* Фон вкладки */
        ads--CDockWidgetTab { background: rgb(40,40,40); }

        /* Текст активної вкладки */
        ads--CDockWidgetTab[activeTab="true"] QLabel { color: white; }

        /* Рамка навколо області доку */
        ads--CDockAreaWidget { border: 1px solid rgb(40,40,40); border-radius: 4px; }

        /* Контейнер вмісту доку */
        ads--CDockWidget > QScrollArea { border: none; }
    """

    LIGHT_STYLE = """
        /* Кнопка закриття на вкладці (приховано) */
        ads--CDockWidgetTab > QPushButton { max-width: 0; max-height: 0; padding: 0; margin: 0; border: none; }

        /* Заголовок області доків */
        ads--CDockAreaTitleBar { background: rgb(240,240,240); min-height: 15px; max-height: 15px; }

        /* Кнопки в заголовку */
        ads--CDockAreaTitleBar QAbstractButton { background: rgb(240,240,240); border: none; }

        /* Текст неактивної вкладки */
        ads--CDockWidgetTab QLabel { background: rgb(240,240,240); color: rgb(100,100,100); }

        /* Фон вкладки */
        ads--CDockWidgetTab { background: rgb(240,240,240); }

        /* Текст активної вкладки */
        ads--CDockWidgetTab[activeTab="true"] QLabel { color: black; }

        /* Рамка навколо області доку */
        ads--CDockAreaWidget { border: 1px solid rgb(200,200,200); border-radius: 4px; }

        /* Контейнер вмісту доку */
        ads--CDockWidget > QScrollArea { border: none; }
    """

    def __init__(self, parent: QWidget, style: str = "dark"):
        super().__init__()
        self._parent = parent
        self._manager: Optional[ads.CDockManager] = None
        self._docks: Dict[str, ads.CDockWidget] = {}
        self._closed: set = set()
        self._style = style

    def setup(self, **flags) -> ads.CDockManager:
        defaults = {
            'OpaqueSplitterResize': True,
            'XmlCompressionEnabled': False,
            'DockAreaHasTabsMenuButton': False,
            'DockAreaHasUndockButton': False,
            'HideSingleCentralWidgetTitleBar': True,
            'MiddleMouseButtonClosesTab': True,
        }
        defaults.update(flags)

        for name, value in defaults.items():
            if hasattr(ads.CDockManager, name):
                ads.CDockManager.setConfigFlag(getattr(ads.CDockManager, name), value)

        self._manager = ads.CDockManager(self._parent)
        self.set_style(self._style)
        return self._manager

    def get_widget(self) -> ads.CDockManager:
        return self._manager

    def add(self, name: str, widget: QWidget, area=None, into: Optional[ads.CDockAreaWidget] = None) -> ads.CDockWidget:
        area = area or ads.RightDockWidgetArea
        dock = ads.CDockWidget(name)
        dock.setWidget(widget)

        self._manager.addDockWidget(area, dock, into) if into else self._manager.addDockWidget(area, dock)
        self._docks[name] = dock

        dock.closed.connect(lambda: self._on_closed(name))
        dock.viewToggled.connect(lambda v: self._on_toggled(name, v))
        return dock

    def _on_closed(self, name: str):
        self._closed.add(name)
        self.dock_closed.emit(name)
        self.state_changed.emit()

    def _on_toggled(self, name: str, visible: bool):
        if visible:
            self._closed.discard(name)
            self.dock_opened.emit(name)
        else:
            self._closed.add(name)
            self.dock_closed.emit(name)

    def get(self, name: str) -> Optional[ads.CDockWidget]:
        return self._docks.get(name)

    def is_open(self, name: str) -> bool:
        return name in self._docks and not self._docks[name].isClosed()

    def toggle(self, name: str, show: bool):
        if name not in self._docks:
            return
        if show:
            self._manager.show()
            self._docks[name].toggleView(True)
            self._closed.discard(name)
        else:
            self._docks[name].toggleView(False)
            self._closed.add(name)
        self.state_changed.emit()

    def show(self, name: str):
        self.toggle(name, True)

    def hide(self, name: str):
        self.toggle(name, False)

    def show_all(self):
        self._manager.show()
        for name in self._docks:
            self._docks[name].toggleView(True)
            self._closed.discard(name)
        self.state_changed.emit()

    def hide_all(self):
        for name in self._docks:
            self._docks[name].toggleView(False)
            self._closed.add(name)
        self._manager.hide()
        self.state_changed.emit()

    def all_docks(self) -> Dict[str, ads.CDockWidget]:
        return self._docks.copy()

    def get_names(self) -> List[str]:
        return list(self._docks.keys())

    def open_names(self) -> List[str]:
        return [n for n in self._docks if self.is_open(n)]

    def closed_names(self) -> List[str]:
        return list(self._closed)

    def save_state(self) -> str:
        return json.dumps({
            'layout': self._manager.saveState().data().hex(),
            'closed': list(self._closed)
        })

    def restore_state(self, state_json: str) -> bool:
        try:
            data = json.loads(state_json)
            self._closed = set(data.get('closed', []))

            if layout := data.get('layout'):
                self._manager.restoreState(QByteArray(bytes.fromhex(layout)))

            for name in self._closed:
                if name in self._docks:
                    self._docks[name].toggleView(False)
            return True
        except Exception as e:
            print(f"DockManager restore error: {e}")
            return False

    def set_style(self, style: str):
        if style == "dark":
            self._manager.setStyleSheet(self.DARK_STYLE)
        elif style == "light":
            self._manager.setStyleSheet(self.LIGHT_STYLE)
        else:
            self._manager.setStyleSheet(style)
        self._style = style
    
    def create_view_menu(self, menu):
        """Додає пункти керування доками в меню."""
        menu.addAction("Показати всі", self.show_all)
        menu.addAction("Сховати всі", self.hide_all)
        menu.addSeparator()

        self._dock_actions = {}
        for name in sorted(self.get_names()):
            action = menu.addAction(name)
            action.setCheckable(True)
            action.setChecked(self.is_open(name))
            action.triggered.connect(lambda checked, n=name: self.toggle(n, checked))
            self._dock_actions[name] = action

        def update_checks():
            for name, action in self._dock_actions.items():
                action.setChecked(self.is_open(name))

        menu.aboutToShow.connect(update_checks)