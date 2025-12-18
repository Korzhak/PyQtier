import can
from typing import Callable, Optional, List
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from .data_processor import CanDataProcessor


class Statuses:
    OK = "OK"
    ERROR = "ERROR"
    DISCONNECTED = "DISCONNECTED"
    TIMEOUT = "TIMEOUT"


class CanModel(QObject):
    devices_list_updated = pyqtSignal()
    message_received = pyqtSignal(object)  # can.Message

    def __init__(self):
        super().__init__()
        self._bus: Optional[can.Bus] = None
        self._interface: str = "systec"
        self._channel: int = 0
        self._device_id: int = 0  # ID адаптера
        self._bitrate: int = 500000
        self._is_connected: bool = False

        self._data_processor: Optional[CanDataProcessor] = None
        self._data_ready_callback: Optional[Callable] = None
        self._error_callback: Optional[Callable] = None
        self._connection_lost_callback: Optional[Callable] = None
        self._connect_callback: Optional[Callable] = None
        self._disconnect_callback: Optional[Callable] = None

        self._listener_thread: Optional[QThread] = None

    def set_can_interface(self, device_available: bool):
        """Встановити параметри для підключення"""
        self._device_id = 0  # Завжди використовуємо Device 0
        self._channel = 0  # Завжди канал 0
        self._interface = "systec"

    def set_channel(self, channel: int):
        """Встановити канал адаптера (0 або 1)"""
        self._channel = channel

    def set_bit_rate(self, bitrate: int):
        """Встановити битрейт"""
        self._bitrate = bitrate

    def connect(self) -> str:
        """Підключитися до Systec CAN адаптера"""
        try:
            from can.interfaces.systec.ucanbus import UcanBus

            # Підключення через UcanBus
            self._bus = UcanBus(
                device=self._device_id,
                channel=self._channel,
                bitrate=self._bitrate
            )
            self._is_connected = True

            # Запускаємо listener для прийому повідомлень
            self._start_listener()

            if self._connect_callback:
                self._connect_callback()

            return Statuses.OK

        except Exception as e:
            if self._error_callback:
                self._error_callback(f"Systec CAN connection error: {str(e)}")
            return Statuses.ERROR

    def disconnect(self):
        """Відключитися від CAN шини"""
        if self._bus:
            self._stop_listener()
            self._bus.shutdown()
            self._bus = None

        self._is_connected = False

        if self._disconnect_callback:
            self._disconnect_callback()

    def send_message(self, can_id: int, data: bytes, extended: bool = False):
        """Відправити CAN повідомлення"""
        if not self._is_connected or not self._bus:
            return False

        try:
            message = can.Message(
                arbitration_id=can_id,
                data=data,
                is_extended_id=extended
            )
            self._bus.send(message)
            return True

        except Exception as e:
            if self._error_callback:
                self._error_callback(f"Send error: {str(e)}")
            return False

    def write(self, data: dict):
        """Відправити дані (альтернативний метод)"""
        can_id = data.get('id', 0)
        payload = data.get('data', b'')
        extended = data.get('extended', False)

        if isinstance(payload, (list, tuple)):
            payload = bytes(payload)
        elif isinstance(payload, str):
            payload = payload.encode()

        return self.send_message(can_id, payload, extended)

    def set_message_filter(self, can_id: int, mask: int = 0x7FF):
        """Встановити фільтр повідомлень"""
        if self._bus:
            try:
                self._bus.set_filters([{"can_id": can_id, "can_mask": mask}])
            except:
                pass

    def is_device_available(self) -> bool:
        """Перевірити чи є доступний Systec пристрій (Device 0)"""
        try:
            from can.interfaces.systec.ucanbus import UcanBus
            # Спробуємо підключитися до Device 0
            test_bus = UcanBus(device=0, channel=0, bitrate=500000)
            test_bus.shutdown()
            return True
        except:
            return False

    def get_device_status(self) -> str:
        """Отримати статус пристрою"""
        if self.is_device_available():
            return "Device Available"
        else:
            return "No Device Found"

    def get_adapter_info(self, device_id: int = 0) -> dict:
        """Отримати детальну інформацію про адаптер"""
        try:
            from can.interfaces.systec.ucanbus import UcanBus

            test_bus = UcanBus(device=device_id, channel=0, bitrate=500000)

            try:
                hw_info, ch0_info, ch1_info = test_bus.get_hardware_info()

                info = {
                    'device_id': device_id,
                    'product_name': getattr(hw_info, 'product_name', 'Unknown'),
                    'serial_number': getattr(hw_info, 'serial_number', 'Unknown'),
                    'firmware_version': getattr(hw_info, 'firmware_version', 'Unknown'),
                    'hardware_version': getattr(hw_info, 'hardware_version', 'Unknown'),
                    'channel_0_available': hasattr(ch0_info, 'can_type'),
                    'channel_1_available': hasattr(ch1_info, 'can_type'),
                    'status': 'Available'
                }

            except Exception as e:
                info = {
                    'device_id': device_id,
                    'status': 'Available (limited info)',
                    'error': str(e)
                }

            test_bus.shutdown()
            return info

        except Exception as e:
            return {
                'device_id': device_id,
                'status': 'Not Available',
                'error': str(e)
            }

    def _start_listener(self):
        """Запустити прослуховування повідомлень"""
        if self._bus:
            from PyQt5.QtCore import QTimer
            self._timer = QTimer()
            self._timer.timeout.connect(self._check_messages)
            self._timer.start(10)  # Перевіряти кожні 10мс

    def _stop_listener(self):
        """Зупинити прослуховування"""
        if hasattr(self, '_timer'):
            self._timer.stop()

    def _check_messages(self):
        """Перевірити нові повідомлення"""
        if not self._bus:
            return

        try:
            message = self._bus.recv(timeout=0)  # Non-blocking
            if message:
                self.message_received.emit(message)

                message
                if self._data_processor:
                    processed_data = self._data_processor.parse(message)
                    if processed_data and self._data_ready_callback:
                        self._data_ready_callback(processed_data)

        except Exception as e:
            # Можливо втрачено з'єднання
            if "disconnected" in str(e).lower():
                if self._connection_lost_callback:
                    self._connection_lost_callback()

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    # Setters для callbacks
    def set_data_processor(self, processor: CanDataProcessor):
        self._data_processor = processor

    def set_data_ready_callback(self, callback: Callable):
        self._data_ready_callback = callback

    def set_error_callback(self, callback: Callable):
        self._error_callback = callback

    def set_connection_lost_callback(self, callback: Callable):
        self._connection_lost_callback = callback

    def set_connect_callback(self, callback: Callable):
        self._connect_callback = callback

    def set_disconnect_callback(self, callback: Callable):
        self._disconnect_callback = callback