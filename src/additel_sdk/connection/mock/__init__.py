# connection/mock/__init__.py

import json
import logging
from ..base import Connection
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.additel_sdk import Additel


class MockConnection(Connection):
    """A mock connection class for testing purposes.

    This connection type uses pre-defined responses from a JSON file to simulate
    device behavior without requiring an actual physical connection.
    """

    type = "mock"
    response_file = "mockADT286.json"
    responses = {}

    def __init__(self, parent: "Additel", **kwargs):
        self.parent = parent
        self.connected = False
        self.ip = kwargs.pop("ip", os.environ.get("ADDITEL_IP"))
        self.use_wlan_fallback = kwargs.pop("use_wlan_fallback")

    def __enter__(self):
        """Simulates connecting to the device."""
        if not MockConnection.responses:
            filepath = os.path.join(os.path.dirname(__file__), self.response_file)
            with open(filepath) as f:
                MockConnection.responses[self.response_file] = json.load(f)
        self.responses = MockConnection.responses[self.response_file]
        self.connected = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Simulates disconnecting from the device."""
        self.connected = False

    def send_command(self, command: str) -> None:
        """Stores the command to be processed by read_response."""
        if not self.connected:
            raise ConnectionError("Not connected to device")

    def read_response(self) -> str:
        """Returns the pre-defined or fallback response for the last command."""

        last_command = self.parent.commands[-1]
        if last_command == "SYSTem:DATE?":
            from datetime import date

            return date.today().strftime("%Y,%m,%d")

        if response := self.responses.get(last_command, None):
            return response

        if self.use_wlan_fallback:
            try:
                from ..wlan import WLANConnection

                with WLANConnection(self.parent, ip=self.ip) as wlan_connection:
                    if response := wlan_connection.cmd(last_command):
                        self.responses[last_command] = response
                        self.save_response(last_command, response)
                        return response
            except Exception as e:
                logging.warning(f"WLAN fallback failed: {e}")
                return None

    @classmethod
    def save_response(cls, command, response):
        """Saves the command and response to the JSON file."""
        filepath = os.path.join(os.path.dirname(__file__), cls.response_file)
        try:
            with open(filepath, "r+") as f:
                data = json.load(f)
                data[command] = response
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        except FileNotFoundError:
            print(f"Warning: Response file not found: {cls.response_file}")
        except Exception as e:
            print(f"Error saving response to file: {e}")
