from PyQt5 import QtWidgets

from gui.ui.settings_interface import Ui_Settings


class SettingsView(Ui_Settings):
    def __init__(self, widget: QtWidgets.QWidget):
        self.widget = widget
        self.setupUi(widget)

        self.__is_opened = False

        self.__add_behaviour()

    def __add_behaviour(self):
        """
        Add callbacks
        :return: None
        """
        # START YOUR CODE
        ...
        # END YOUR CODE

    def open(self):
        """
        Open the settings window
        :return: None
        """
        self.widget.show()
        self.__is_opened = True

    def close(self):
        """
        Close the settings window
        :return: None
        """
        self.widget.close()
        self.__is_opened = False

    @property
    def is_opened(self):
        """
        Check if the settings window is opened
        :return: True if the settings window is opened else false
        """
        return self.__is_opened
