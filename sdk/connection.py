# connection/__init__.py
from .wlan_connection import WLANConnection
from .usb_connection import USBConnection
from .serial_connection import SerialConnection
from .bluetooth_connection import BluetoothConnection
from .ethernet_connection import EthernetConnection

class Connection:
    """Class to handle different ways of connecting to the device."""
    def __init__(self, parent, connection_type, **kwargs):
        self.parent = parent
        self.connType = connection_type
        if connection_type == 'wlan':
            assert 'ip' in kwargs, "IP address is required for WLAN connection."
            self.connection = WLANConnection(parent, **kwargs)
        
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

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def connect(self):
        self.connection.connect()
    
    def disconnect(self):
        self.connection.disconnect()
