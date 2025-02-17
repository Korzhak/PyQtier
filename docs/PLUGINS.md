# Working with plugins

Plugin is an additional program which extends opportunities of module and doesn't need changing module's code.

List of plugins:

- **UsbPlugin**. Created for quick development application with USB connection.

### UsbPlugin (writing in progress)

1. Importing

```python
from app.utils.data_parser import DataParser
from pyqtier.plugins.usb_plugin import UsbPluginManager
```

```python
self.usb_data_parser = DataParser()

self.usb_manager = UsbPluginManager(with_baudrate=True)
self.usb_manager.setup_view(self.main_window.ui.widget, self.main_window.ui.statusbar)
self.usb_manager.set_data_parser(self.usb_data_parser)
self.usb_manager.set_obtain_data_callback(self.main_window.obtain_usb_data)

self.main_window.set_send_callback(self.usb_manager.send)
```

