from typing import Callable, Optional

from .auxiliary import *
from .models.data_processor import CanDataProcessor
from .models.can_model import CanModel, Statuses
from ..plugins import PyQtierPlugin


class CanPluginManager(PyQtierPlugin):
    def __init__(self, with_bitrate: bool = False, default_bitrate: int = 500000, custom_ui=None):
        super().__init__()

        if with_bitrate:
            from .views.can_control_with_bitrate import Ui_CanWidget
            self._default_bitrate: int = default_bitrate
        else:
            from .views.can_control import Ui_CanWidget
            self._default_bitrate: int = 0

        self._with_bitrate: bool = with_bitrate

        if custom_ui:
            self._ui = custom_ui()
        else:
            self._ui = Ui_CanWidget()

        self._can: CanModel = CanModel()
        self._external_lost_connection_callback: Optional[Callable] = None

    def setup_view(self, *args, **kwargs):
        super().setup_view(*args, **kwargs)

        # Виводимо інфо про CAN в статусбар
        self.update_can_status()

        if self._with_bitrate:
            self._ui.cb_list_bit_rates.addItems(BITRATES_LIST)
            self._ui.cb_list_bit_rates.setCurrentIndex(BITRATES_LIST.index(str(self._default_bitrate)))

        self.create_behavior()

    def create_behavior(self):
        self._ui.bt_connect_disconnect.clicked.connect(self._connect_disconnect_callback)

    def send_data(self, data: dict):
        self._can.write(data)

    def send_message(self, can_id: int, data: bytes, extended: bool = False):
        """Відправити CAN повідомлення"""
        self._can.send_message(can_id, data, extended)

    def update_can_status(self):
        """Оновити CAN статус в статусбарі"""
        if self._can.is_device_available():
            status = "CAN: Systec device available"
        else:
            status = "CAN: No Systec device found"

        if self._statusbar:
            self._statusbar.showMessage(status)

    # ===== SETTERS =====
    def set_obtain_data_callback(self, callback):
        self._can.set_data_ready_callback(callback)

    def set_error_callback(self, callback):
        self._can.set_error_callback(callback)

    def set_connection_lost_callback(self, callback):
        self._external_lost_connection_callback = callback
        self._can.set_connection_lost_callback(self._lost_connection_callback)

    def set_connect_callback(self, callback: Callable):
        self._can.set_connect_callback(callback)

    def set_disconnect_callback(self, callback: Callable):
        self._can.set_disconnect_callback(callback)

    def set_data_processor(self, data_processor: CanDataProcessor):
        self._can.set_data_processor(data_processor)

    def set_message_filter(self, can_id: int, mask: int = 0x7FF):
        """Встановити фільтр повідомлень CAN"""
        self._can.set_message_filter(can_id, mask)

    # ===== INTERNAL METHODS =====
    def _connect(self):
        # Встановлюємо параметри підключення
        self._can.set_can_interface(True)

        # Встановлюємо битрейт якщо потрібно
        if self._with_bitrate:
            bitrate = int(self._ui.cb_list_bit_rates.currentText())
            self._can.set_bit_rate(bitrate)

        # Спробуємо підключитися
        if self._can.connect() == Statuses.OK:
            self._ui.bt_connect_disconnect.setText("Disconnect")
            if self._statusbar:
                bitrate_info = f" @ {bitrate}kbps" if self._with_bitrate else ""
                self._statusbar.showMessage(f"CAN: Connected to Systec device{bitrate_info}")
        else:
            if self._statusbar:
                self._statusbar.showMessage("CAN: Connection failed!")

    def _disconnect(self):
        if self._can.is_connected:
            self._can.disconnect()

        self._ui.bt_connect_disconnect.setText("Connect")

        if self._statusbar:
            self._statusbar.showMessage("CAN: Disconnected")

    def _connect_disconnect_callback(self):
        if self._can.is_connected:
            self._disconnect()
        else:
            self._connect()

    def _lost_connection_callback(self):
        self._disconnect()
        if self._statusbar:
            self._statusbar.showMessage("CAN: Connection lost!")

        if self._external_lost_connection_callback:
            self._external_lost_connection_callback()