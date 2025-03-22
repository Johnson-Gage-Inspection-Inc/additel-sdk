# connection/__init__.py
from .connections.wlan import WLANConnection

from .connections.usb import USBConnection
from .connections.serial import SerialConnection
from .connections.bluetooth import BluetoothConnection
from .connections.ethernet import EthernetConnection


class Connection:
    """Class to handle different ways of connecting to the device."""

    def __init__(self, parent, connection_type, **kwargs):
        self.parent = parent
        self.connType = connection_type
        if connection_type == "wlan":
            self.connection = WLANConnection(self, **kwargs)

        elif connection_type == 'usb':
            assert 'port' in kwargs, "Port is required for USB connection."
            self.connection = USBConnection(parent, **kwargs)

        elif connection_type == 'serial':
            assert 'port' in kwargs, "Port is required for Serial connection."
            self.connection = SerialConnection(parent, **kwargs)

        elif connection_type == 'bluetooth':
            assert 'port' in kwargs, "Port is required for Bluetooth connection."
            self.connection = BluetoothConnection(parent, **kwargs)

        elif connection_type == 'ethernet':
            assert 'ip' in kwargs, "IP address is required for Ethernet connection."
            self.connection = EthernetConnection(parent, **kwargs)

        else:
            raise ValueError(f"Connection type '{connection_type}' is not supported.")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def connect(self):
        self.connection.connect()

    def disconnect(self):
        self.connection.disconnect()
