# __init__.py - Base class for Additel SDK.
from .module import Module
from .scan import Scan
from .channel import Channel
from .connection import Connection

# from .calibration import Calibration
# from .system import System
# from .program import Program
# from .display import Display, Diagnostic
# from .pattern import Pattern
# from .unit import Unitfrom .channel import DIFunctionChannelConfig as DFCC

import logging


class Additel:
    """Base class for interacting with an Additel device using different connection types."""

    def __init__(self, connection_type="wlan", **kwargs):
        self.connection_type = connection_type
        self.connection = Connection(self, connection_type, **kwargs)

        # Initialize the submodules
        self.Module = Module(self)
        self.Scan = Scan(self)
        self.Channel = Channel(self)
        # self.Calibration = Calibration(self)
        # self.System = System(self)
        # self.Program = Program(self)
        # self.Display = Display(self)
        # self.Diagnostic = Diagnostic(self)
        # self.Pattern = Pattern(self)
        # self.Unit = Unit(self)

    def __enter__(self):
        self.connection.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.disconnect()

    def send_command(self, command) -> None:
        """Send a command to the connected device and return the response."""
        try:
            if hasattr(self.connection.connection, "send_command"):
                self.connection.connection.send_command(command)
            else:
                raise NotImplementedError(
                    "The current connection type does not support sending commands."
                )
        except Exception as e:
            logging.error(f"Error sending command '{command}': {e}")
            raise

    def read_response(self) -> str:
        """Read the response from the connected device."""
        try:
            if hasattr(self.connection.connection, "read_response"):
                return self.connection.connection.read_response()
            else:
                raise NotImplementedError(
                    "The current connection type does not support reading responses."
                )
        except Exception as e:
            logging.error(f"Error reading response: {e}")
            raise

    def cmd(self, command) -> str:
        self.send_command(command)
        return self.read_response()

    # Section 1 - Commands Instruction

    # Section 1.1 - IEEE488.2 common commands

    # 1.1.1 *CLS - Clear Status Command
    def clear_status(self) -> None:
        """Clear the device status.

        This command eliminates the following registers:
        - Standard event register
        - Querying event register
        - Operating event register
        - Status byte register
        - Error queue
        """
        self.send_command("*CLS")

    # 1.1.2
    def identify(self) -> str:
        """Query the device identification.

        This command queries the instrument's identification details. The returned data is divided into two parts:
        - Product sequence number
        - Software version number

        Returns:
            str: A string containing the product sequence number and software version number.
        """
        return self.cmd("*IDN?")

    # 1.1.3
    def reset(self) -> None:
        """Perform a software reset.

        This command resets the device's main software, reinitializing its state.
        """
        self.send_command("*RST")
