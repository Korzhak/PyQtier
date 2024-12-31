# !/usr/bin/env python
"""
Utility for running PyQtier desktop applications.
"""

from app.windows_manager import WindowsManager
from core.widgets.registry import WidgetRegistry


def main():
    try:
        from PyQt5 import QtCore
    except ImportError as exc:
        raise ImportError("Couldn't import PyQt5. Are you sure it's installed?") from exc
    wm = WindowsManager()
    wm.show_ui()


if __name__ == '__main__':
    main()
