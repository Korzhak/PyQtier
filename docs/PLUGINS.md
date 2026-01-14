# Working with plugins

Plugin is an additional program which extends opportunities of module and doesn't need changing module's code.

List of plugins:

- **UsbPlugin**. Created for quick development application with USB connection.
- **CanPlugin**. Created for quick development application with CAN bus connection (Systec devices).
- **ModbusPlugin**. Created for quick development application with Modbus RTU communication.

---

## UsbPlugin

### Description
Plugin for managing USB serial communication with automatic port detection and optional baudrate configuration.

### Initialization

```python
from pyqtier.plugins.usb_plugin import UsbPluginManager, UsbDataProcessor
```

### Basic Setup

```python
# Without baudrate selection
usb_manager = UsbPluginManager()

# With baudrate selection
usb_manager = UsbPluginManager(with_baudrate=True, default_baudrate=9600)

# Setup view
usb_manager.setup_view(widget, statusbar)
```

### Using Data Processor

```python
from pyqtier.plugins.usb_plugin import UsbDataProcessor

class MyDataProcessor(UsbDataProcessor):
    def process_data(self, raw_data: bytes) -> dict:
        # Process incoming data
        return {"parsed": raw_data.decode()}

data_processor = MyDataProcessor()
usb_manager.set_data_processor(data_processor)
```

### Sending Data

```python
# Send data through USB
usb_manager.send_data({"command": "start"})
```

### Available Signals

```python
usb_manager.connected.connect(on_connected)
usb_manager.disconnected.connect(on_disconnected)
usb_manager.connection_lost.connect(on_connection_lost)
usb_manager.error_occurred.connect(on_error)
usb_manager.raw_data_received.connect(on_raw_data)
usb_manager.data_ready.connect(on_obtain_data)
usb_manager.devices_list_updated.connect(on_devices_updated)
```

### Static Methods

```python
# Get available USB ports
available_ports = UsbPluginManager.get_available_ports()
```

---

## CanPlugin

### Description
Plugin for managing CAN bus communication with Systec devices. Supports message filtering, custom bitrates, and automatic device detection.

### Initialization

```python
from pyqtier.plugins.can_plugin import CanPluginManager, CanDataProcessor
```

### Basic Setup

```python
# Without bitrate selection
can_manager = CanPluginManager()

# With bitrate selection
can_manager = CanPluginManager(with_bitrate=True, default_bitrate=500000)

# Setup view
can_manager.setup_view(widget, statusbar)
```

### Using Data Processor

```python
from pyqtier.plugins.can_plugin import CanDataProcessor

class MyCanDataProcessor(CanDataProcessor):
    def process_data(self, message: dict) -> dict:
        # Process CAN message: {'id': int, 'data': bytes, 'extended': bool}
        return {"processed_message": message}

data_processor = MyCanDataProcessor()
can_manager.set_data_processor(data_processor)
```

### Sending CAN Messages

```python
# Send standard CAN message
can_manager.send_message(can_id=0x123, data=b'\x01\x02\x03\x04')

# Send extended CAN message
can_manager.send_message(can_id=0x18FF1234, data=b'\x01\x02', extended=True)

# Send using dict format
can_manager.send_data({"id": 0x123, "data": b'\x01\x02'})
```

### Message Filtering

```python
# Set filter for specific CAN ID
can_manager.set_message_filter(can_id=0x123, mask=0x7FF)
```

### Device Information

```python
# Check if device is available
is_available = can_manager.is_device_available()

# Get adapter info
adapter_info = can_manager.get_adapter_info(device_id=0)
```

### Available Signals

```python
can_manager.connected.connect(on_connected)
can_manager.disconnected.connect(on_disconnected)
can_manager.connection_lost.connect(on_connection_lost)
can_manager.error_occurred.connect(on_error)
can_manager.message_received.connect(on_message)
can_manager.data_ready.connect(on_obtain_data)
can_manager.devices_list_updated.connect(on_devices_updated)
```

---

## ModbusPlugin

### Description
Plugin for managing Modbus RTU communication over serial ports. Supports reading/writing holding registers, input registers, coils, and discrete inputs with automatic polling.

### Initialization

```python
from pyqtier.plugins.modbus_plugin import ModbusPluginManager, ModbusDataProcessor
```

### Basic Setup

```python
# With baudrate selection (default)
modbus_manager = ModbusPluginManager(
    with_baudrate=True,
    default_baudrate=9600,
    default_slave_id=1
)

# Setup view
modbus_manager.setup_view(widget, statusbar)
```

### Using Data Processor with Auto-Polling

```python
from pyqtier.plugins.modbus_plugin import ModbusDataProcessor

class MyModbusDataProcessor(ModbusDataProcessor):
    def __init__(self):
        super().__init__()
        self.modbus_manager = None

    def set_modbus_manager(self, manager):
        self.modbus_manager = manager

    def poll_data(self):
        # Called automatically when polling is active
        if self.modbus_manager:
            data = self.modbus_manager.read_holding_registers(address=0, count=10)
            if data:
                self.process_data(data)

    def process_data(self, data):
        # Process the received data
        print(f"Received: {data}")

data_processor = MyModbusDataProcessor()
modbus_manager.set_data_processor(data_processor)
# Polling starts automatically on connection
```

### Reading Data

```python
# Read holding registers (function code 3)
values = modbus_manager.read_holding_registers(address=100, count=5, slave_id=1)

# Read input registers (function code 4)
values = modbus_manager.read_input_registers(address=200, count=3)

# Read coils (function code 1)
states = modbus_manager.read_coils(address=0, count=8)

# Read discrete inputs (function code 2)
states = modbus_manager.read_discrete_inputs(address=10, count=4)

# Universal read method
values = modbus_manager.read(function_code=3, address=100, count=5, slave_id=1)
```

### Writing Data

```python
# Write single register (function code 6)
success = modbus_manager.write_register(address=100, value=1234)

# Write multiple registers (function code 16)
success = modbus_manager.write_registers(address=100, values=[10, 20, 30])

# Write single coil (function code 5)
success = modbus_manager.write_coil(address=0, value=True)

# Write multiple coils (function code 15)
success = modbus_manager.write_coils(address=0, values=[True, False, True])

# Universal write method
success = modbus_manager.write(function_code=6, address=100, value=1234, slave_id=1)
```

### Device Information

```python
# Get available serial ports
ports = ModbusPluginManager.get_available_ports()

# Get current slave ID from UI
current_slave_id = modbus_manager.get_slave_id()
```

### Available Signals

```python
modbus_manager.connected.connect(on_connected)
modbus_manager.disconnected.connect(on_disconnected)
modbus_manager.connection_lost.connect(on_connection_lost)
modbus_manager.error_occurred.connect(on_error)
modbus_manager.data_ready.connect(on_obtain_data)
modbus_manager.devices_list_updated.connect(on_devices_updated)
```

### Notes
- Slave ID can be set in UI or passed as parameter to each method
- Valid slave ID range: 1-247
- Data processor automatically starts/stops polling on connect/disconnect
- All read methods return `None` on error

