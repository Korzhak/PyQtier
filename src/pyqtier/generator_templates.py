TEMPLATES = {
    'main.py': '''# !/usr/bin/env python
"""
Utility for running PyQtier desktop applications.
"""

from app.windows_manager import WindowsManager


def main():
    try:
        from PyQt5 import QtCore
    except ImportError as exc:
        raise ImportError("Couldn't import PyQt5. Are you sure it's installed?") from exc
    wm = WindowsManager()
    wm.show_ui()


if __name__ == '__main__':
    main()
''',

    'app/windows_manager.py': '''# -*- coding: utf-8 -*-
from pyqtier import PyQtierWindowsManager

from app.models import SettingsModel
from app.templates import Ui_MainWindow
from app.views import MainWindowView


class WindowsManager(PyQtierWindowsManager):
    def __init__(self):
        super().__init__()
        self.settings_window = None

    def setup_manager(self):
        self.setup_main_window(Ui_MainWindow, MainWindowView, SettingsModel)

        # Creating windows widgets
        self.settings_window = self.widget_registry.get_initialized_widget('settings_widget')

        self.main_window.register_callback('settings_widget', self.settings_window.open)

        # Adding behaviours to widgets (must be the last section)
        self.main_window.add_behaviour()


    ''',

    'app/models/__init__.py': '''from .settings import SettingsModel''',

    'app/models/settings.py': '''from pyqtier.models import PyQtierSettingsModel


class SettingsModel(PyQtierSettingsModel):
    def __init__(self, settings_id: str = ""):
        super(SettingsModel, self).__init__(settings_id)
''',

    'app/views/__init__.py': '''
from .windows_widgets import *
from .main_window_view import MainWindowView
    ''',

    'app/views/main_window_view.py': '''from pyqtier.views import PyQtierMainWindowView


class MainWindowView(PyQtierMainWindowView):
    def add_behaviour(self):
        self.ui.actionSettings.triggered.connect(self.get_callback('settings_widget'))
''',

    'app/views/windows_widgets.py': '''from app.models.settings import SettingsModel
from pyqtier.registry import PyQtierWidgetRegistry
from app.templates import Ui_SimpleView
from pyqtier.views import PyQtierSimpleView


@PyQtierWidgetRegistry.register("settings_widget", Ui_SimpleView, SettingsModel)
class SettingsWidget(PyQtierSimpleView):
    ...
''',

    'app/templates/__init__.py': '''from .main_window_interface import Ui_MainWindow
from .simple_interface import Ui_SimpleView
    ''',

    'app/templates/simple_interface.py': '''# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SimpleView(object):
    def setupUi(self, SimpleView):
        SimpleView.setObjectName("SimpleView")
        SimpleView.resize(400, 300)

        self.retranslateUi(SimpleView)
        QtCore.QMetaObject.connectSlotsByName(SimpleView)

    def retranslateUi(self, SimpleView):
        _translate = QtCore.QCoreApplication.translate
        SimpleView.setWindowTitle(_translate("SimpleView", "SimpleView"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SimpleView = QtWidgets.QWidget()
    ui = Ui_SimpleView()
    ui.setupUi(SimpleView)
    SimpleView.show()
    sys.exit(app.exec_())
''',

    'app/templates/main_window_interface.py': '''# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.bt1 = QtWidgets.QPushButton(self.centralwidget)
        self.bt1.setGeometry(QtCore.QRect(310, 110, 113, 32))
        self.bt1.setObjectName("bt1")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyQtier Main Window"))
        self.bt1.setText(_translate("MainWindow", "PushButton"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
''',
}
