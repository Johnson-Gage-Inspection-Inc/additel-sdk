import json
from .wlan import WLANConnection  
import logging

class MockConnection:
    """A mock connection class for testing purposes.
    
    This connection type uses pre-defined responses from a JSON file to simulate
    device behavior without requiring an actual physical connection.
    """
    
    def __init__(self, parent, response_file='tests/mockADT286.json', ip=None, **kwargs):
        self.parent = parent
        self.response_file = response_file
        self.connected = False
        self._responses = {}
        self.wlan_connection = None  # Initialize wlan_connection
        self.ip = ip  # Store the IP address
        
    def connect(self):
        """Simulates connecting to the device."""
        try:
            with open(self.response_file) as f:
                self._responses = json.load(f)
            self.connected = True
        except FileNotFoundError:
            raise FileNotFoundError(f"Mock responses file not found: {self.response_file}")
        
        # If IP is provided, initialize WLAN connection for fallback
        if self.ip:
            try:
                self.wlan_connection = WLANConnection(self.parent, ip=self.ip)
            except Exception as e:
                print(f"Warning: Could not initialize WLAN connection: {e}")
                self.wlan_connection = None

    def disconnect(self):
        """Simulates disconnecting from the device."""
        self.connected = False
        if self.wlan_connection:
            self.wlan_connection.disconnect()

    def send_command(self, command: str) -> str:
        """Simulates sending a command and returns the pre-defined response."""
        if not self.connected:
            raise ConnectionError("Not connected to device")
        self.last_command = command

    def read_response(self) -> str:
        """Returns the pre-defined response for the last sent command."""
        return self._responses.get(self.last_command)

    def cmd(self, command):
        """Send a command to the device and return the response."""
        if not self.connected:
            raise ConnectionError("Not connected to device")
        
        response = self._responses.get(command)
        
        if response is None and self.wlan_connection:
            try:
                response = self.wlan_connection.cmd(command)
                if response:  # Check for a non-trivial response
                    self._responses[command] = response
                    self._save_response(command, response)  # Save the new command/response pair
                return response
            except Exception as e:
                logging.warning(f"WLAN fallback failed: {e}")
                return
        
        # Return the fake response if available, otherwise return OK
        return response

    def _save_response(self, command, response):
        """Saves the command and response to the JSON file."""
        try:
            with open(self.response_file, 'r+') as f:
                data = json.load(f)
                data[command] = response
                f.seek(0)  # Go back to the beginning of the file
                json.dump(data, f, indent=4)
                f.truncate()  # Remove any remaining part of the old file
        except FileNotFoundError:
            print(f"Warning: Response file not found: {self.response_file}")
        except Exception as e:
            print(f"Error saving response to file: {e}")
