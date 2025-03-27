# __init__.py - Base class for Additel SDK.
import logging
from traceback import print_tb
from time import time, sleep

from .module import Module
from .scan import Scan
from .channel import Channel
from .connection import Connection
# from .calibration import Calibration
from .system import System
# from .program import Program
# from .display import Display, Diagnostic
# from .pattern import Pattern
from .unit import Unit
from .errors import AdditelError


class ConnectionTypeFilter(logging.Filter):
    def __init__(self, conn_type):
        super().__init__()
        self.conn_type = conn_type

    def filter(self, record):
        record.connection_type = self.conn_type
        return True


logging.basicConfig(
    filename="additel.log",
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] (%(connection_type)s) %(message)s',
    force=True
)


class Additel:
    """Base class for interacting with an Additel device using different connection
    types.
    """

    def __init__(self, connection_type="wlan", **kwargs):
        self.type = connection_type
        _logger = logging.getLogger()
        if not any(isinstance(f, ConnectionTypeFilter) for f in _logger.filters):
            _logger.addFilter(ConnectionTypeFilter(self.type))
        self.connection = Connection(self, connection_type=self.type, **kwargs)

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

        self.command_log = []
        logging.debug(f"Additel initialized with connection type: {connection_type}")

    def __enter__(self):
        self.connection.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"Exception type: {exc_type}")
            print(f"Exception value: {exc_value}")
            print_tb(traceback)
        self.connection.__exit__(exc_type, exc_value, traceback)

    def send_command(self, command: str) -> None:
        """Send a command to the connected device and return the response."""
        self.connection.send_command(command.strip())
        self.command_log.append(command)
        logging.info(f"Command: {command}")
        self.wait_for_operation_complete()
        error = self.System.get_error()
        if error.error_code != 0:
            raise AdditelError(**error)

    def read_response(self) -> str:
        try:
            response = self.connection.read_response()
            logging.info(f"Response: {response}")
            return response
        except TimeoutError as e:
            try:
                raise AdditelError(**self.System.get_error()) from e
            except Exception as nested:
                msg = "Failed to retrieve error details after timeout."
                raise RuntimeError(msg) from nested

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
        psn, svn = self.cmd("*IDN?").split(",")
        return {
            "Product Sequence Number": psn[1:-1],
            "Software Version Number": svn,
        }

    # 1.1.3
    def reset(self) -> None:
        """Perform a software reset.

        This command resets the device's main software, reinitializing its state.
        """
        self.send_command("*RST")

    def wait_for_operation_complete(self, timeout=30):
        """Wait for the *OPC? command to return '1' indicating completion.

        Args:
            timeout (int): Maximum time (in seconds) to wait for completion.

        Raises:
            TimeoutError: If the operation does not complete before timing out.
        """
        start_time = time()
        while time() - start_time < timeout:
            response = self.opc()
            if response == '1':
                logging.info("Operation complete.")
                return True
            sleep(1)  # Wait for 1 second before retrying
        raise TimeoutError("Operation did not complete within the timeout period.")

    def opc(self) -> str:
        """Send an operation complete query (*OPC?) and return the response.

        Returns:
            str: The response to the *OPC? command, usually "1" if operations complete.
        """
        return self.cmd("*OPC?")

    # Not in the manual:
    def get_event_status_enable(self) -> dict:
        """Query and interpret the Standard Event Status Enable Register (*ESE?)."""
        raw = int(self.cmd("*ESE?"))
        parsed = self.parse_status_register(raw)
        logging.info(f"*ESE? = {raw:08b} => {parsed}")
        return parsed

    def get_event_status_register(self) -> dict:
        """Query and interpret the Standard Event Status Register (*ESR?)."""
        raw = int(self.cmd("*ESR?"))
        parsed = self.parse_status_register(raw)
        logging.info(f"*ESR? = {raw:08b} => {parsed}")
        return parsed

    # Table 4-3 Standard Event Register Bit Definition
    def parse_status_register(self, value: int) -> dict:
        """Parse a standard SCPI 488.2 status register bitmask."""
        bits = {
            7: "Power On",
            6: "User Request",  # Unused
            5: "Command Error",  # Unused
            4: "Execution Error",
            3: "Device-Specific Error",
            2: "Query Error",
            1: "Request Control",  # Unused
            0: "Operation Complete",
        }
        return {
            name: bool(value & (1 << bit))
            for bit, name in bits.items()
        }
