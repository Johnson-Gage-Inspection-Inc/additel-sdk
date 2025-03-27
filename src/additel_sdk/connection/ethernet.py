import socket
from . import Connection
from json import loads, JSONDecodeError


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

    def __enter__(self):
        """Establish a socket connection to the device."""
        try:
            self.socket = socket.create_connection(
                (self.ip_address, self.port), timeout=self.timeout
            )
        except socket.error as e:
            raise ConnectionError(
                f"Failed to __enter__ to {self.ip_address}:{self.port} - {e}"
            ) from e

    def __exit__(self):
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

    def read_response(self, chunk_size=16384) -> str:
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
