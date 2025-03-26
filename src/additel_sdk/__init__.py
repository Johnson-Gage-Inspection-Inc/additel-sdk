# __init__.py - Base class for Additel SDK.
from .module import Module
from .scan import Scan
from .module.channel import Channel
from .connection import Connection

# from .calibration import Calibration
from .system import System
# from .program import Program
# from .display import Display, Diagnostic
# from .pattern import Pattern
from .unit import Unit

from traceback import print_tb


class Additel:
    """Base class for interacting with an Additel device using different connection
    types.
    """

    def __init__(self, connection_type="wlan", **kwargs):
        self.connection = Connection(self, connection_type = connection_type, **kwargs)

        # Initialize the submodules
        self.Module = Module(self)
        self.Scan = Scan(self)
        self.Channel = Channel(self)
        # self.Calibration = Calibration(self)
        self.System = System(self)
        # self.Program = Program(self)
        # self.Display = Display(self)
        # self.Diagnostic = Diagnostic(self)
        # self.Pattern = Pattern(self)
        self.Unit = Unit(self)

        self.commands = []

    def __enter__(self):
        self.connection.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"Exception type: {exc_type}")
            print(f"Exception value: {exc_value}")
            print_tb(traceback)
        self.connection.__exit__(exc_type, exc_value, traceback)

    def send_command(self, command) -> None:
        """Send a command to the connected device and return the response."""
        self.connection.send_command(command)
        self.commands.append(command)

    def read_response(self) -> str:
        """Read the response from the connected device."""
        return self.connection.read_response()

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

        This command queries the instrument's identification details. The returned data
        is divided into two parts:
        - Product sequence number
        - Software version number

        Returns:
            str: A string containing the product sequence number and software version
            number.
        """
        return self.cmd("*IDN?")

    # 1.1.3
    def reset(self) -> None:
        """Perform a software reset.

        This command resets the device's main software, reinitializing its state.
        """
        self.send_command("*RST")
