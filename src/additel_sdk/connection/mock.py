import json


class MockConnection:
    """A mock connection class for testing purposes.
    
    This connection type uses pre-defined responses from a JSON file to simulate
    device behavior without requiring an actual physical connection.
    """
    
    def __init__(self, parent, response_file='tests/mockADT286.json', **kwargs):
        self.parent = parent
        self.response_file = response_file
        self.connected = False
        self._responses = {}
        
    def connect(self):
        """Simulates connecting to the device."""
        try:
            with open(self.response_file) as f:
                self._responses = json.load(f)
            self.connected = True
        except FileNotFoundError:
            raise FileNotFoundError(f"Mock responses file not found: {self.response_file}")
        
    def disconnect(self):
        """Simulates disconnecting from the device."""
        self.connected = False

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
        
        # Return the fake response if available, otherwise return OK
        return self._responses.get(command)