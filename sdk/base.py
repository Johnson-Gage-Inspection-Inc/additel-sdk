import logging
from connection import Connection

class Additel:
    """Base class for interacting with an Additel device using different connection types."""

    def __init__(self, connection_type='wlan', **kwargs):
        self.connection_type = connection_type
        self.connection = Connection(self, connection_type, **kwargs)

    def __enter__(self):
        self.connection.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.disconnect()

    def send_command(self, command):
        """Send a command to the connected device and return the response."""
        try:
            if hasattr(self.connection.connection, 'send_command'):
                self.connection.connection.send_command(command)
            else:
                raise NotImplementedError("The current connection type does not support sending commands.")
        except Exception as e:
            logging.error(f"Error sending command '{command}': {e}")
            raise

    def read_response(self):
        """Read the response from the connected device."""
        try:
            if hasattr(self.connection.connection, 'read_response'):
                return self.connection.connection.read_response()
            else:
                raise NotImplementedError("The current connection type does not support reading responses.")
        except Exception as e:
            logging.error(f"Error reading response: {e}")
            raise

    def cmd(self, command):
        self.send_command(command)
        return self.read_response()

    ## Section 1 - Commands Instruction

    ### Section 1.1 - IEEE488.2 common commands

    # 1.1.1 *CLS - Clear Status Command
    def clear_status(self):  # NOTE: Not tested
        """Clear the device status.

        This command eliminates the following registers:
        - Standard event register
        - Querying event register
        - Operating event register
        - Status byte register
        - Error queue

        Args:
            None

        Returns:
            None
        """
        self.send_command("*CLS")

    # 1.1.2
    def identify(self) -> str:  # Tested!
        """Query the device identification.

        This command queries the instrument's identification details. The returned data is divided into two parts:
        - Product sequence number
        - Software version number

        Args:
            None

        Returns:
            str: A string containing the product sequence number and software version number.
        """
        return self.cmd("*IDN?")

    # 1.1.3
    def reset(self):  # NOTE: Not tested
        """Perform a software reset.

        This command resets the device's main software, reinitializing its state.

        Args:
            None

        Returns:
            None
        """
        self.send_command("*RST")
