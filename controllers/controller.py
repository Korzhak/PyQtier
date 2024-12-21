# -*- coding: utf-8 -*-
from core.controllers import AbstractController
from models.settings import Settings
from views.main_window_view import MainWindowView


class Controller(AbstractController):
    def __init__(self):
        super(Controller, self).__init__()
        self.settings = Settings()

        self.view = MainWindowView(self.main_window, self.settings)
