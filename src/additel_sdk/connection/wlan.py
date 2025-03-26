# Connection class for Additel devices over WLAN.
import logging
import socket
import os
from traceback import print_tb
from . import Connection


class WLANConnection(Connection):
    type = "wlan"

    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.ip = kwargs.pop("ip", os.environ.get("ADDITEL_IP"))
        self.port = kwargs.pop("port", 8000)
        self.timeout = kwargs.pop("timeout", 1)
        self.connection = None

    def __enter__(self):
        """Establish a connection to the Additel device."""
        self.connection = None
        try:
            self.connection = socket.create_connection(
                (self.ip, self.port), timeout=self.timeout
            )
            return self
        except Exception as e:
            logging.error(f"Error connecting to Additel device: {e}")
            raise e

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection to the Additel device."""
        if exc_type is not None:
            print(f"Exception type: {exc_type}")
            print(f"Exception value: {exc_value}")
            print_tb(traceback)
        if self.connection:
            self.connection.close()
            self.connection = None

    def send_command(self, command: str):
        """Send a command to the Additel device."""
        try:
            self.connection.sendall(f"{command}\n".encode())
        except Exception as e:
            logging.error(f"Error sending command '{command}': {e}")
            raise e

    def read_response(self, bufsize=16384) -> str:
        """Read the response from the connected device."""

        try:
            return self.connection.recv(bufsize).decode().strip()
        except Exception as e:
            logging.error(f"Error reading response: {e}")
            raise e
