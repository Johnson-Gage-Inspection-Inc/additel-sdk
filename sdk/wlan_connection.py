# Connection class for Additel devices over WLAN.
import logging
import socket

class WLANConnection:
    def __init__(self, ip: str, **kwargs):
        self.ip = ip
        self.port: int = kwargs.get('port', 8000)
        self.timeout: int = kwargs.get('timeout', 1)
        if unused_kwargs := set(kwargs.keys()) - {'port', 'timeout', 'ip'}:
            logging.warning(f"Invalid keyword arguments: {unused_kwargs}")
        self.connection = None
        self.connect()
            
    def connect(self):
        """Establish a connection to the Additel device."""
        try:
            self.connection = socket.create_connection((self.ip, self.port), timeout=self.timeout)
        except Exception as e:
            logging.error(f"Error connecting to Additel device: {e}")
            raise e

    def disconnect(self):
        """Close the connection to the Additel device."""
        if self.connection:
            self.connection.close()
            self.connection = None