import json
from typing import Dict, List, Optional

from PyQt5.QtCore import QByteArray, QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget

try:
    from PyQtAds import ads
except ImportError:
    raise ImportError("PyQtAds is required. Install: pip install PyQtAds")

from pyqtier.static.qss import styles


class PyQtierDockManager(ads.CDockManager):

    CONFIG_DEFAULTS = {
        'OpaqueSplitterResize': True,
        'XmlCompressionEnabled': False,
        'DockAreaHasTabsMenuButton': False,
        'DockAreaHasUndockButton': False,
        'HideSingleCentralWidgetTitleBar': True,
        'MiddleMouseButtonClosesTab': True,
    }

    def __init__(self, parent: QWidget, style: str = "dark", **flags):
        config = self.CONFIG_DEFAULTS.copy()
        config.update(flags)

        for name, value in config.items():
            if hasattr(ads.CDockManager, name):
                ads.CDockManager.setConfigFlag(getattr(ads.CDockManager, name), value)

        super().__init__(parent)
        self._docks: Dict[str, ads.CDockWidget] = {}
        self._closed: set = set()
        self._style = style
        self.set_style(self._style)

        if parent.layout():
            parent.layout().addWidget(self)

    def add(self, name: str, widget: QWidget, area=None, into: Optional[ads.CDockAreaWidget] = None) -> ads.CDockWidget:
        area = area or ads.RightDockWidgetArea
        dock = ads.CDockWidget(name)
        dock.setWidget(widget)

        self.addDockWidget(area, dock, into) if into else self.addDockWidget(area, dock)
        self._docks[name] = dock

        dock.closed.connect(lambda: self._on_closed(name))
        dock.viewToggled.connect(lambda v: self._on_toggled(name, v))
        return dock

    def _on_closed(self, name: str):
        self._closed.add(name)

    def _on_toggled(self, name: str, visible: bool):
        if visible:
            self._closed.discard(name)
        else:
            self._closed.add(name)

    def get(self, name: str) -> Optional[ads.CDockWidget]:
        return self._docks.get(name)

    def is_open(self, name: str) -> bool:
        return name in self._docks and not self._docks[name].isClosed()

    def toggle(self, name: str, show: bool):
        if name not in self._docks:
            return
        if show:
            super().show()
            self._docks[name].toggleView(True)
            self._closed.discard(name)
        else:
            self._docks[name].toggleView(False)
            self._closed.add(name)

    def show(self, name: str):
        self.toggle(name, True)

    def hide(self, name: str):
        self.toggle(name, False)

    def show_all(self):
        super().show()
        for name in self._docks:
            self._docks[name].toggleView(True)
            self._closed.discard(name)

    def hide_all(self):
        for name in self._docks:
            self._docks[name].toggleView(False)
            self._closed.add(name)
        super().hide()

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
            'layout': self.saveState().data().hex(),
            'closed': list(self._closed)
        })

    def restore_state(self, state_json: str) -> bool:
        try:
            data = json.loads(state_json)
            self._closed = set(data.get('closed', []))

            if layout := data.get('layout'):
                self.restoreState(QByteArray(bytes.fromhex(layout)))

            for name in self._closed:
                if name in self._docks:
                    self._docks[name].toggleView(False)
            return True
        except Exception as e:
            print(f"DockManager restore error: {e}")
            return False

    def set_style(self, style: str):
        if style == "dark":
            self.setStyleSheet(styles.DOCK_DARK_STYLE)
        elif style == "light":
            self.setStyleSheet(styles.DOCK_LIGHT_STYLE)
        else:
            self.setStyleSheet(style)
        self._style = style

    def create_view_menu(self, menu: QMenu):
        """Додає пункти керування доками в меню."""
        menu.addSeparator()
        self._dock_actions = {}
        for name in sorted(self.get_names()):
            action = menu.addAction(name)
            action.setCheckable(True)
            action.setChecked(self.is_open(name))
            action.triggered.connect(lambda checked, n=name: self.toggle(n, checked))
            self._dock_actions[name] = action
        menu.addSeparator()
        menu.addAction("Показати всі", self.show_all)
        menu.addAction("Сховати всі", self.hide_all)


        def update_checks():
            for name, action in self._dock_actions.items():
                action.setChecked(self.is_open(name))

        menu.aboutToShow.connect(update_checks)
