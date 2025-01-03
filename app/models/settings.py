from core.models import PyQtierSettingsModel


class SettingsModel(PyQtierSettingsModel):
    def __init__(self, settings_id: str = ""):
        super(SettingsModel, self).__init__(settings_id)
