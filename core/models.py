# -*- coding: utf-8 -*-
from configparser import ConfigParser

import auxiliary


class SettingsModel(object):
    def __init__(self):
        self._config = ConfigParser()
        self._defaults = auxiliary.CONFIG_DEFAULTS
        self._config.read(auxiliary.CONFIG_FILE_PATH)
        self.load_configs()

    def load_configs(self) -> None:
        """
        Load configuration from file
        :return: None
        """
        try:
            for section in auxiliary.CONFIG_SECTIONS:
                if section not in self._config.sections():
                    self._config.add_section(section)
            self._ui = self._config["UI"]
        except KeyError as err:
            raise KeyError(f"Key '{err}' does not exist in config file")

    def update_config_file(self) -> None:
        """
        Update configuration or create new config file
        :return: None
        """
        with open(auxiliary.CONFIG_FILE_PATH, 'w') as configfile:
            self._config.write(configfile)

    @property
    def main_window_size(self) -> tuple:
        """
        :return: tuple (width, height)
        """
        return tuple(map(int, self._ui.get("main_window_size",
                                           fallback=self._defaults["main_window_size"]).split('x')))

    @property
    def main_window_position(self) -> tuple:
        """
        :return: tuple (x, y)
        """
        return tuple(map(int, self._ui.get("main_window_position",
                                           fallback=self._defaults["main_window_position"]).split(",")))

    # START YOUR OWN GETTER METHODS

    ...

    # END YOUR OWN GETTER METHODS

    def set_main_window_size(self, width, height) -> None:
        """
        Saving main window size parameters
        :param width: width of main window (px)
        :param height: height of main window (px)
        :return: None
        """
        self._config.set("UI", "main_window_size", f"{width}x{height}")
        self.update_config_file()

    def set_main_window_position(self, x, y) -> None:
        """
        Saving main window position parameters
        :param x: x position of main window (px)
        :param y: y position of main window (px)
        :return: None
        """
        self._config.set("UI", "main_window_position", f"{x},{y}")
        self.update_config_file()

    # START YOUR OWN SETTER METHODS

    ...

    # END YOUR OWN SETTER METHODS
