import json
import logging
from . import Connection


class MockConnection(Connection):
    """A mock connection class for testing purposes.

    This connection type uses pre-defined responses from a JSON file to simulate
    device behavior without requiring an actual physical connection.
    """
    type = "mock"

    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.response_file = kwargs.pop("response_file")
        self.connected = False
        self._responses = {}
        self.ip = kwargs.pop("ip", None)
        self.use_wlan_fallback = kwargs.pop("use_wlan_fallback")

    def __enter__(self):
        """Simulates connecting to the device."""
        try:
            with open(self.response_file) as f:
                self._responses = json.load(f)
            self.connected = True
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Mock responses file not found: {self.response_file}"
            ) from e


    def __exit__(self):
        """Simulates disconnecting from the device."""
        self.connected = False

    def send_command(self, command: str) -> None:
        """Stores the command to be processed by read_response."""
        if not self.connected:
            raise ConnectionError("Not connected to device")
        self.last_command = command

    def read_response(self) -> str:
        """Returns the pre-defined or fallback response for the last command."""
        if self.last_command == "SYSTem:DATE?":
            from datetime import date
            return date.today().strftime("%Y,%m,%d")
        response = self._responses.get(self.last_command)
        self.last_command = None
        if response is None and self.use_wlan_fallback:
            try:
                from .wlan import WLANConnection
                with WLANConnection(self.parent, ip=self.ip) as wlan_connection:
                    response = wlan_connection.cmd(self.last_command)
                    if response:  # Save only non-trivial responses
                        self._responses[self.last_command] = response
                        self._save_response(self.last_command, response)
            except Exception as e:
                logging.warning(f"WLAN fallback failed: {e}")
                return None

        return response


    def _save_response(self, command, response):
        """Saves the command and response to the JSON file."""
        try:
            with open(self.response_file, "r+") as f:
                data = json.load(f)
                data[command] = response
                f.seek(0)  # Go back to the beginning of the file
                json.dump(data, f, indent=4)
                f.truncate()  # Remove any remaining part of the old file
        except FileNotFoundError:
            print(f"Warning: Response file not found: {self.response_file}")
        except Exception as e:
            print(f"Error saving response to file: {e}")
