import socket
from . import Connection


class EthernetConnection(Connection):
    """Class to handle Ethernet connection to the device."""
    type = "ethernet"

    def __init__(self, parent, **kwargs):
        self.ip_address = kwargs.get("ip")
        self.port = kwargs.get("port", 5025)  # Default port for SCPI devices
        self.timeout = kwargs.get("timeout", 10)  # Default timeout in seconds
        self.socket = None

        if not self.ip_address:
            raise ValueError("IP address is required for Ethernet connection.")

    def connect(self):
        """Establish a socket connection to the device."""
        try:
            self.socket = socket.create_connection(
                (self.ip_address, self.port), timeout=self.timeout
            )
        except socket.error as e:
            raise ConnectionError(
                f"Failed to connect to {self.ip_address}:{self.port} - {e}"
            ) from e

    def disconnect(self):
        """Close the socket connection."""
        if self.socket:
            try:
                self.socket.close()
                self.socket = None
            except socket.error as e:
                raise ConnectionError(f"Failed to close connection - {e}") from e

    def send_command(self, command):
        """Send a command to the device over the socket connection."""
        if not self.socket:
            raise ConnectionError("Ethernet connection is not established.")

        try:
            self.socket.sendall(f"{command}\n".encode())
        except socket.error as e:
            raise IOError(f"Failed to send command '{command}' - {e}") from e

    def read_response(self):
        """Read a response from the device."""
        if not self.socket:
            raise ConnectionError("Ethernet connection is not established.")

        try:
            response = self.socket.recv(4096).decode().strip()
            return response
        except socket.error as e:
            raise IOError(f"Failed to read response - {e}") from e
