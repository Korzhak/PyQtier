# !/usr/bin/env python
"""
Utility for running PyQtier desktop applications.
"""

from controllers.controller import Controller


def main():
    try:
        from PyQt5 import QtCore
    except ImportError as exc:
        raise ImportError("Couldn't import PyQt5. Are you sure it's installed?") from exc
    c = Controller()
    c.show_ui()


if __name__ == '__main__':
    main()
