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
            """Acquire module information.

            This command retrieves information about the front panel and junction box modules.

            Parameters:
                None

            Returns:
                str: A semicolon-separated string containing module information, with each parameter separated by commas.
                The response includes:
                - Identifier of the box (0 for front panel, 1 for embedded junction box, etc.)
                - Box serial number
                - Box type (0 for front panel, 1 for temperature box, etc.)
                - Box hardware version
                - Box software version
                - Total number of box channels
                - Label of the box
            """
            response = self.parent.send_command("JSON:MODule:INFormation?")
            if response:
                return [DIModuleInfo(**module) for module in json.loads(response)]
            return []

        def set_label(self, index: int, label: str):
            """Set the label of a specific junction box module.

            This command assigns a custom label to a specified module.

            Parameters:
                index (int): The identifier of the junction box. Values:
                    - 0: Front panel
                    - 1: Embedded junction box
                    - 2, 3, 4: Serial-wound junction boxes
                label (str): The label to assign to the module (enclosed in quotation marks).

            Returns:
                None
            """
            command = f'MODule:LABel {index},"{label}"'
            self.parent.send_command(command)

        def get_configuration(self, module_index: int) -> List[DIFunctionChannelConfig]:
            """Acquire channel configuration of a specified junction box.

            This command retrieves the channel configuration for a specified junction box module.

            Parameters:
                module_index (int): The identifier of the module to query. Values:
                    - 0: Front panel
                    - 1: Embedded junction box
                    - 2, 3, 4: Serial-wound junction boxes

            Returns:
                List[DIFunctionChannelConfig]: A list of channel configurations for the specified module.
            """
            response = self.parent.send_command(f"JSON:MODule:CONFig? {module_index}")
            if response:
                return [DIFunctionChannelConfig(**config) for config in json.loads(response)]
            return []

        def configure(self, module_index: int, params: List[DIFunctionChannelConfig]):
            """Set the channel configuration of a specified junction box in JSON format.

            This command configures the channel settings for a specified module using JSON.

            Parameters:
                module_index (int): The identifier of the module to configure. Values:
                    - 0: Front panel
                    - 1: Embedded junction box
                    - 2, 3, 4: Serial-wound junction boxes
                params (dict): A dictionary containing channel configurations. Each channel's configuration includes:
                    - Channel name
                    - Enable or not (0 or 1)
                    - Label
                    - Function type:
                        0 = Voltage, 1 = Current, 2 = Resistance, 3 = RTD, 4 = Thermistor, 
                        100 = TC, 101 = Switch, 102 = SPRT, 103 = Voltage Transmitter, 
                        104 = Current Transmitter, 105 = Standard TC, 106 = Custom RTD, 
                        110 = Standard Resistance
                    - Range index
                    - Channel delay
                    - Automatic range (0 or 1)
                    - Filter settings
                    - Additional parameters based on electrical logging type:
                        * Voltage: High impedance or not
                        * Current: None
                        * Resistance: Wires, positive/negative current
                        * RTD/SPRT/Custom RTD: Sensor name, wires, compensation interval, 
                            1.4x current setting
                        * Thermistor: Sensor name, wires, sensor serial number, sensor ID
                        * TC/Standard TC: Break detection, sensor name, sensor serial number, 
                            cold junction type, fixed value, custom junction channel name
                        * Current/Voltage Transmitters: Wires, sensor name, sensor serial number, 
                            sensor ID

            Returns:
                dict: The JSON response from the device confirming the configuration.
            """
            json_params = json.dumps([param.__dict__ for param in params])
            command = f'JSON:MODule:CONFig {module_index},{json_params}'
            self.parent.send_command(command)

    class Scan:
        def __init__(self, parent):
            self.parent = parent

        def start(self, scan_info: DIScanInfo):
            """Set the configuration and start scanning.

            This command configures the scanning parameters and starts the scan.

            Parameters:
                params (str): A comma-separated string containing:
                    - NPLC (Number of Power Line Cycles)
                    - Sample work frequency cycle (100, 1000, or 4000)
                    - Channel name

            Returns:
                None
            """
            json_params = json.dumps(scan_info.__dict__)
            command = f'JSON:SCAN:STARt {json_params}'
            self.parent.send_command(command)

        def get_configuration(self) -> DIScanInfo:
            """Acquire the scanning configuration.

            This command retrieves the current scanning configuration, including:
                - NPLC (Number of Power Line Cycles)
                - The name of the current scanning channel

            Parameters:
                None

            Returns:
                str: A comma-separated string containing the scanning configuration:
                    - NPLC value
                    - Channel name
            """
            response = self.parent.send_command("JSON:SCAN:STARt?")
            if response:
                return DIScanInfo(**json.loads(response))
            return None

        def stop(self):
            """Stop scanning.

            This command stops any active scanning process on the device.

            Parameters:
                None

            Returns:
                None
            """
            self.parent.send_command("SCAN:STOP")

        def get_latest_data(self, time_format: Optional[str] = None) -> Optional[str]:
            """Acquire the most recent scanning data.

            This command retrieves the latest scanning data for all active channels. Optionally, the `time` parameter specifies
            the desired timestamp format:
                - 1: "yyyy:MM:dd HH:mm:ss fff" format
                - 2: Long format

            Parameters:
                time (str, optional): Timestamp format. Defaults to an empty string, indicating no specific time format.

            Returns:
                str: A semicolon-separated string where each entry represents data for a channel. Each entry includes:
                    - For Electrical Measurement Data:
                        * Channel name
                        * Electrical unit ID
                        * Number of electrical measurement data
                        * Electrical measurement data
                        * Filtered electrical measurement data
                    - For Temperature Data:
                        * Channel name
                        * Electrical unit ID
                        * Number of electrical measurement data
                        * Electrical measurement data
                        * Filtered electrical measurement data
                        * Indication unit ID
                        * Number of indication data
                        * Indication data
                    - For TC Data:
                        * Channel name
                        * Electrical unit ID
                        * Number of electrical measurement data
                        * Electrical measurement data
                        * Filtered electrical measurement data
                        * Indication unit ID
                        * Number of indication data
                        * Indication data
                        * Cold junction electrical unit ID
                        * Cold junction electrical test data
                        * Cold junction temperature unit ID
                        * Cold junction temperature data
                    - For Switch Data:
                        * Status data (based on TC or RTD data)
                    - For Voltage/Current Transmitter Data:
                        * Channel name
                        * Electrical unit ID
                        * Number of electrical measurement data
                        * Electrical measurement data
                        * Filtered electrical measurement data
                        * Input signal unit ID
                        * Input signal name
                        * Number of input signals
                        * Input signal data
            """
            command = "SCAN:DATA:Last?"
            if time_format:
                command += f" {time_format}"
            return self.parent.send_command(command)

        def get_data_json(self, count: int) -> List[dict]:
            """Acquire scanning data in JSON format.

            This command retrieves scanning data in JSON format for the specified number of data points.

            Parameters:
                count (int): The number of scanning data points to retrieve.

            Returns:
                dict: A dictionary representation of the scanning data. Each entry includes:
                    - Channel name
                    - Electrical measurement data
                    - Filtered data
                    - Additional parameters depending on the measurement type
            """
            command = f"JSON:SCAN:DATA? {count}"
            response = self.parent.send_command(command)
            if response:
                return json.loads(response)
            return []

    class Channel:
        def __init__(self, parent):
            self.parent = parent

        def get_configuration(self, channel_name: str) -> DIFunctionChannelConfig:
            """Acquire the configuration of a specific channel.

            This command retrieves the configuration for a specified channel.

            Parameters:
                channel_name (str): The name of the channel to query.

            Returns:
                str: A comma-separated string containing channel configuration, including:
                    - Channel name
                    - Enable or not (0 or 1)
                    - Label
                    - Function type
                    - Range index
                    - Channel delay
                    - Automatic range (0 or 1)
                    - Number of filters
                    - m additional parameters, based on the type of electrical measurement:
                        * Voltage (m=1): High impedance or not
                        * Current (m=0): None
                        * Resistance (m=2): Wires, open positive/negative current
                        * RTD/SPRT/Custom RTD (m=6): Wires, sensor name, sensor serial number, sensor ID, 
                        whether to open 1.4x current, compensation interval
                        * Thermistors (m=4): Wires, sensor name, sensor serial number, sensor ID
                        * TC/Standard TC (m=7): Break detection, sensor name, sensor serial number, sensor ID,
                        cold junction type, cold junction fixed value, custom cold junction channel name
                        * Current/Voltage Transmitters (m=4): Wires, sensor name, sensor serial number, sensor ID
            """
            response = self.parent.send_command(f'JSON:CHANnel:CONFig? "{channel_name}"')
            if response:
                return DIFunctionChannelConfig(**json.loads(response))
            return None

        def configure(self, channel_config: DIFunctionChannelConfig):
            """Acquire channel configuration in JSON format.

            This command retrieves configuration data for one or more channels in JSON format.

            Parameters:
                channel_names (DIFunctionChannelConfig): A list of channel configurations. Each configuration includes:
                    channel_name (str): The name of the channel to configure.
                    enabled (int): Enable or disable the channel (1 for enabled, 0 for disabled).
                    label (str): A custom label for the channel.
                    func_type (int): Function type, with the following values:
                        - 0: Voltage
                        - 1: Current
                        - 2: Resistance
                        - 3: RTD
                        - 4: Thermistor
                        - 100: Thermocouple (TC)
                        - 101: Switch
                        - 102: SPRT
                        - 103: Voltage Transmitter
                        - 104: Current Transmitter
                        - 105: Standard TC
                        - 106: Custom RTD
                        - 110: Standard Resistance
                    range_index (int): The range index for the channel.
                    delay (int): Channel delay.
                    auto_range (int): Automatic range setting (1 for enabled, 0 for disabled).
                    filters (int): Number of filters.
                    other_params (str): Additional parameters based on the function type:
                        - Voltage: High impedance or not.
                        - Current: None.
                        - Resistance: Wires, whether to open positive and negative current.
                        - RTD/SPRT/Custom RTD: Sensor name, wires, sensor serial number, sensor ID, 
                        whether to open 1.4 times current, compensation interval.
                        - Thermistor: Sensor name, wires, sensor serial number, sensor ID.
                        - TC/Standard TC: Break detection, sensor name, sensor serial number, 
                        sensor ID, cold junction type (0 internal, 1 external, 2 custom), 
                        cold end fixed value, external cold junction channel name.
                        - Switch: Switch type.
                        - Current/Voltage Transmitter: Wires, sensor name, sensor serial number, sensor ID.

            Returns:
                None
            """
            json_params = json.dumps(channel_config.__dict__)
            command = f'JSON:CHANnel:CONFig {json_params}'
            self.parent.send_command(command)

        def set_zero(self, enable: bool):
            """Enable or disable zero clearing for a single channel.

            This command sets or cancels zero clearing for a specific channel.

            Parameters:
                enable (int): 1 to enable zero clearing, 0 to cancel.

            Returns:
                None
            """
            command = f"CHANnel:ZERo {int(enable)}"
            self.parent.send_command(command)
