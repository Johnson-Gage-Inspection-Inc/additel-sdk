# Description: Base class for Additel

import socket
from typing import Optional
import time
import json
from .module import Module
from .scan import Scan
from .channel import Channel
from .calibration import Calibration
from .system import System
from .program import Program
from .display import Display, Diagnostic
from .pattern import Pattern
from .unit import Unit

class Additel:
    def __init__(self, ip: str, port: int = 8000, timeout: int = 10, retries: int = 1):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.retries = retries
        self.connection = None
        self.Module = Module(self)
        self.Scan = Scan(self)
        self.Channel = Channel(self)
        self.Calibration = Calibration(self)
        self.System = System(self)
        self.Program = Program(self)
        self.Display = Display(self)
        self.Diagnostic = Diagnostic(self)
        self.Pattern = Pattern(self)
        self.Unit = Unit(self)

    def __enter__(self):
        # Enable use of the class in a context manager to ensure proper resource handling
        self.connect()  # FIXME: Enable the use of USB, Ethernet, and other connection types
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Ensure the connection is closed when exiting the context
        self.disconnect()

    def connect(self):
        """Establish a connection to the Additel device."""
        try:
            # Create a socket connection to the device
            self.connection = socket.create_connection((self.ip, self.port), timeout=self.timeout)
        except Exception as e:
            print(f"Error connecting to Additel device: {e}")

    def disconnect(self):
        """Close the connection to the Additel device."""
        if self.connection:
            # Safely close the socket connection
            self.connection.close()
            self.connection = None

    def send_command(self, command: str) -> Optional[str]:
        """Send a command to the Additel device and receive the response, with retry logic."""
        for attempt in range(self.retries):
            try:
                if not self.connection:
                    # Re-establish the connection if it's not active
                    self.connect()
                # Send the command to the device, ensuring proper newline termination
                self.connection.sendall(f"{command}\n".encode())
                # Receive the response, with a buffer size sufficient for JSON data
                return self.connection.recv(4096).decode().strip()
            except socket.timeout:
                # Handle command timeout and retry if necessary
                print(f"Timeout on attempt {attempt + 1} for command '{command}'. Retrying...")
                time.sleep(1)  # Introduce a delay before retrying
            except Exception as e:
                # Handle other exceptions and abort retries
                print(f"Error sending command '{command}': {e}")
                break
        return None  # Return None if all retries fail

    def parse_json(self, response: str) -> dict:
        """Parse a JSON response from the device.

        Parameters:
            response (str): The JSON string received from the device.

        Returns:
            dict: The parsed JSON as a Python dictionary, or an empty dictionary if parsing fails.
        """
        try:
                # Attempt to parse the JSON response
            return json.loads(response)
        except json.JSONDecodeError as e:
                # Log an error if parsing fails
            print(f"Error decoding JSON response: {e}")
        return {}  # Return an empty dictionary for invalid or missing responses

    # Wrapped commands:

    ## Section 1 - Commands Instruction

    ### Section 1.1 - IEEE488.2 common commands
    def clear_status(self):
        """Clear the device status.

        This command eliminates the following registers:
        - Standard event register
        - Querying event register
        - Operating event register
        - Status byte register
        - Error queue

        Parameters:
            None

        Returns:
            None
        """
        self.send_command("*CLS")

    def identify(self):
        """Query the device identification.

        This command queries the instrument's identification details. The returned data is divided into two parts:
        - Product sequence number
        - Software version number

        Parameters:
            None

        Returns:
            str: A string containing the product sequence number and software version number.
        """
        return self.send_command("*IDN?")

    def reset(self):
        """Perform a software reset.

        This command resets the device's main software, reinitializing its state.

        Parameters:
            None

        Returns:
            None
        """
        self.send_command("*RST")