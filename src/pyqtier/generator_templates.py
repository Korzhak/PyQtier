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

    'app/templates/ui/main_window_interface.ui': '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>823</width>
    <height>649</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>PyQtier Main Window</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QGridLayout" name="gridLayout_3">
    <item row="0" column="1">
     <widget class="QGroupBox" name="groupBox">
      <property name="maximumSize">
       <size>
        <width>300</width>
        <height>16777215</height>
       </size>
      </property>
      <property name="title">
       <string>Інтерфейси</string>
      </property>
      <layout class="QGridLayout" name="gridLayout">
       <item row="0" column="0">
        <widget class="QLabel" name="label_2">
         <property name="text">
          <string>UART 1</string>
         </property>
        </widget>
       </item>
       <item row="0" column="1">
        <widget class="QLabel" name="lb_uart1_status">
         <property name="text">
          <string>Не тестовано</string>
         </property>
        </widget>
       </item>
       <item row="0" column="2">
        <widget class="QPushButton" name="pushButton">
         <property name="text">
          <string>Тест</string>
         </property>
        </widget>
       </item>
       <item row="1" column="0">
        <widget class="QLabel" name="label_3">
         <property name="text">
          <string>UART 2</string>
         </property>
        </widget>
       </item>
       <item row="1" column="1">
        <widget class="QLabel" name="lb_uart2_status">
         <property name="text">
          <string>Не тестовано</string>
         </property>
        </widget>
       </item>
       <item row="1" column="2">
        <widget class="QPushButton" name="pushButton_2">
         <property name="text">
          <string>Тест</string>
         </property>
        </widget>
       </item>
       <item row="2" column="0">
        <widget class="QLabel" name="label_4">
         <property name="text">
          <string>SPI 1</string>
         </property>
        </widget>
       </item>
       <item row="2" column="1">
        <widget class="QLabel" name="lb_spi1_status">
         <property name="text">
          <string>Не тестовано</string>
         </property>
        </widget>
       </item>
       <item row="2" column="2">
        <widget class="QPushButton" name="pushButton_3">
         <property name="text">
          <string>Тест</string>
         </property>
        </widget>
       </item>
       <item row="3" column="0">
        <widget class="QLabel" name="label_5">
         <property name="text">
          <string>CAN 1</string>
         </property>
        </widget>
       </item>
       <item row="3" column="1">
        <widget class="QLabel" name="lb_can1_status">
         <property name="text">
          <string>Не тестовано</string>
         </property>
        </widget>
       </item>
       <item row="3" column="2">
        <widget class="QPushButton" name="pushButton_4">
         <property name="text">
          <string>Тест</string>
         </property>
        </widget>
       </item>
       <item row="4" column="0">
        <widget class="QLabel" name="label_6">
         <property name="text">
          <string>CAN 2</string>
         </property>
        </widget>
       </item>
       <item row="4" column="1">
        <widget class="QLabel" name="lb_can2_status">
         <property name="text">
          <string>Не тестовано</string>
         </property>
        </widget>
       </item>
       <item row="4" column="2">
        <widget class="QPushButton" name="pushButton_5">
         <property name="text">
          <string>Тест</string>
         </property>
        </widget>
       </item>
      </layout>
     </widget>
    </item>
    <item row="0" column="0">
     <widget class="QGroupBox" name="groupBox_4">
      <property name="title">
       <string>Загальне</string>
      </property>
      <layout class="QGridLayout" name="gridLayout_4">
       <item row="0" column="0">
        <widget class="QLabel" name="label_8">
         <property name="text">
          <string>Напруга</string>
         </property>
        </widget>
       </item>
       <item row="1" column="0">
        <widget class="QLabel" name="label_9">
         <property name="text">
          <string>Частота</string>
         </property>
        </widget>
       </item>
      </layout>
     </widget>
    </item>
    <item row="1" column="0" colspan="2">
     <widget class="QGroupBox" name="groupBox_2">
      <property name="minimumSize">
       <size>
        <width>0</width>
        <height>200</height>
       </size>
      </property>
      <property name="title">
       <string>Аналогові сигнали</string>
      </property>
     </widget>
    </item>
    <item row="0" column="2" rowspan="2">
     <widget class="QGroupBox" name="groupBox_3">
      <property name="maximumSize">
       <size>
        <width>300</width>
        <height>16777215</height>
       </size>
      </property>
      <property name="title">
       <string>SD</string>
      </property>
      <layout class="QGridLayout" name="gridLayout_2">
       <item row="2" column="1">
        <widget class="QLineEdit" name="lineEdit_2"/>
       </item>
       <item row="4" column="0" colspan="2">
        <widget class="Line" name="line">
         <property name="orientation">
          <enum>Qt::Horizontal</enum>
         </property>
        </widget>
       </item>
       <item row="2" column="0">
        <widget class="QLabel" name="label_7">
         <property name="text">
          <string>Текст</string>
         </property>
        </widget>
       </item>
       <item row="0" column="1">
        <widget class="QLineEdit" name="lineEdit"/>
       </item>
       <item row="5" column="0" colspan="2">
        <widget class="QTreeWidget" name="treeWidget">
         <column>
          <property name="text">
           <string notr="true">1</string>
          </property>
         </column>
        </widget>
       </item>
       <item row="3" column="0" colspan="2">
        <widget class="QPushButton" name="pushButton_6">
         <property name="text">
          <string>Створити файл та додати текст</string>
         </property>
        </widget>
       </item>
       <item row="8" column="0" colspan="2">
        <widget class="QTextBrowser" name="textBrowser"/>
       </item>
       <item row="0" column="0">
        <widget class="QLabel" name="label">
         <property name="text">
          <string>Назва файлу</string>
         </property>
        </widget>
       </item>
       <item row="6" column="0" colspan="2">
        <widget class="QPushButton" name="pushButton_7">
         <property name="text">
          <string>Отримати вміст SD-карти</string>
         </property>
        </widget>
       </item>
       <item row="7" column="0" colspan="2">
        <widget class="QLabel" name="label_10">
         <property name="text">
          <string>Текст в файлі</string>
         </property>
        </widget>
       </item>
      </layout>
     </widget>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>823</width>
     <height>21</height>
    </rect>
   </property>
   <widget class="QMenu" name="menuFile">
    <property name="title">
     <string>File</string>
    </property>
    <addaction name="actionSettings"/>
    <addaction name="separator"/>
    <addaction name="actionQuit"/>
   </widget>
   <addaction name="menuFile"/>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
  <action name="actionSettings">
   <property name="text">
    <string>Settings</string>
   </property>
  </action>
  <action name="actionQuit">
   <property name="text">
    <string>Quit</string>
   </property>
   <property name="shortcut">
    <string>Ctrl+Q</string>
   </property>
  </action>
 </widget>
 <resources/>
 <connections/>
</ui>''',
    
    'app/templates/ui/simple_interface.ui': '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>SimpleView</class>
 <widget class="QWidget" name="SimpleView">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>300</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>SimpleView</string>
  </property>
 </widget>
 <resources/>
 <connections/>
</ui>'''
}
