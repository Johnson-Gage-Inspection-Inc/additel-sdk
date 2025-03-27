# Connection class for Additel devices over WLAN.
import logging
import socket
import os
from traceback import print_tb
from . import Connection
from json import loads, JSONDecodeError


class WLANConnection(Connection):
    type = "wlan"

    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.ip = kwargs.pop("ip", os.environ.get("ADDITEL_IP"))
        self.port = kwargs.pop("port", 8000)
        self.timeout = kwargs.pop("timeout", 1)
        self.socket = None

    def __enter__(self):
        """Establish a connection to the Additel device."""
        self.socket = None
        try:
            self.socket = socket.create_connection(
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
        if self.socket:
            self.socket.close()
            self.socket = None

    def send_command(self, command: str):
        """Send a command to the Additel device."""
        try:
            self.socket.sendall(f"{command}\n".encode())
        except Exception as e:
            logging.error(f"Error sending command '{command}': {e}")
            raise e

    def read_response(self, chunk_size=4096) -> str:
        """Read the response from the connected device in chunks until complete."""
        response = ""
        while chunk := self.socket.recv(chunk_size):
            try:
                response += chunk.decode()
            except UnicodeDecodeError:
                continue
            response = response.strip()
            if not response.startswith('{"$type":'):
                # If the response does not appear to be a JSON object, return it
                return response
            try:
                loads(response)
                return response
            except JSONDecodeError:
                continue
