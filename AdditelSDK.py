import socket
from typing import List, Optional
from customTypes import DIModuleInfo, DIFunctionChannelConfig, DIScanInfo
import time
import json

class Additel:
    def __init__(self, ip: str, port: int = 8000, timeout: int = 10, retries: int = 1):
        # Initialize the Additel connection parameters
        self.ip = ip  # IP address of the device
        self.port = port  # Port number for the device
        self.timeout = timeout  # Timeout for socket connections
        self.retries = retries  # Number of retry attempts for commands
        self.connection = None  # Placeholder for the connection object
        self.module = self.Module(self)
        self.scan = self.Scan(self)
        self.channel = self.Channel(self)

    def __enter__(self):
        # Enable use of the class in a context manager to ensure proper resource handling
        self.connect()
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

    ## 1 Commands Instruction

    ### 1.1 IEEE488.2 common commands
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

    class Module:
        def __init__(self, parent):
            self.parent = parent

        def info(self) -> List[DIModuleInfo]:
            response = self.parent.send_command("JSON:MODule:INFormation?")
            if response:
                return [DIModuleInfo(**module) for module in json.loads(response)]
            return []

        def set_label(self, index: int, label: str):
            command = f'MODule:LABel {index},"{label}"'
            self.parent.send_command(command)

        def get_configuration(self, module_index: int) -> List[DIFunctionChannelConfig]:
            response = self.parent.send_command(f"JSON:MODule:CONFig? {module_index}")
            if response:
                return [DIFunctionChannelConfig(**config) for config in json.loads(response)]
            return []

        def configure(self, module_index: int, params: List[DIFunctionChannelConfig]):
            json_params = json.dumps([param.__dict__ for param in params])
            command = f'JSON:MODule:CONFig {module_index},{json_params}'
            self.parent.send_command(command)

    class Scan:
        def __init__(self, parent):
            self.parent = parent

        def start(self, scan_info: DIScanInfo):
            json_params = json.dumps(scan_info.__dict__)
            command = f'JSON:SCAN:STARt {json_params}'
            self.parent.send_command(command)

        def get_configuration(self) -> DIScanInfo:
            response = self.parent.send_command("JSON:SCAN:STARt?")
            if response:
                return DIScanInfo(**json.loads(response))
            return None

        def stop(self):
            self.parent.send_command("SCAN:STOP")

        def get_latest_data(self, time_format: Optional[str] = None) -> Optional[str]:
            command = "SCAN:DATA:Last?"
            if time_format:
                command += f" {time_format}"
            return self.parent.send_command(command)

        def get_data_json(self, count: int) -> List[dict]:
            command = f"JSON:SCAN:DATA? {count}"
            response = self.parent.send_command(command)
            if response:
                return json.loads(response)
            return []

    class Channel:
        def __init__(self, parent):
            self.parent = parent

        def get_configuration(self, channel_name: str) -> DIFunctionChannelConfig:
            response = self.parent.send_command(f'JSON:CHANnel:CONFig? "{channel_name}"')
            if response:
                return DIFunctionChannelConfig(**json.loads(response))
            return None

        def configure(self, channel_config: DIFunctionChannelConfig):
            json_params = json.dumps(channel_config.__dict__)
            command = f'JSON:CHANnel:CONFig {json_params}'
            self.parent.send_command(command)

        def set_zero(self, enable: bool):
            command = f"CHANnel:ZERo {int(enable)}"
            self.parent.send_command(command)
