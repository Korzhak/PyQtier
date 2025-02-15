# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Projects\Python\CableTester\app\templates\ui\usb_control_with_baudrate.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UsbWidget(object):
    def setupUi(self, UsbWidget):
        UsbWidget.setObjectName("UsbWidget")
        UsbWidget.resize(400, 99)
        self.horizontalLayout = QtWidgets.QHBoxLayout(UsbWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(UsbWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.cb_list_usb_devices = ExtendedComboBox(self.frame)
        self.cb_list_usb_devices.setObjectName("cb_list_usb_devices")
        self.gridLayout.addWidget(self.cb_list_usb_devices, 1, 0, 1, 1)
        self.cb_list_baud_rates = QtWidgets.QComboBox(self.frame)
        self.cb_list_baud_rates.setObjectName("cb_list_baud_rates")
        self.gridLayout.addWidget(self.cb_list_baud_rates, 1, 1, 1, 1)
        self.bt_connect_disconnect = QtWidgets.QPushButton(self.frame)
        self.bt_connect_disconnect.setObjectName("bt_connect_disconnect")
        self.gridLayout.addWidget(self.bt_connect_disconnect, 1, 2, 1, 1)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(UsbWidget)
        QtCore.QMetaObject.connectSlotsByName(UsbWidget)

    def retranslateUi(self, UsbWidget):
        _translate = QtCore.QCoreApplication.translate
        UsbWidget.setWindowTitle(_translate("UsbWidget", "USB"))
        self.label.setText(_translate("UsbWidget", "USB Device"))
        self.label_2.setText(_translate("UsbWidget", "Baud rate"))
        self.label_3.setText(_translate("UsbWidget", "Connection lost"))
        self.bt_connect_disconnect.setText(_translate("UsbWidget", "Connect"))


from pyqtier.widgets import ExtendedComboBox
