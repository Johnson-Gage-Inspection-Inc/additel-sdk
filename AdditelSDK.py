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
        self.calibration = self.Calibration(self)

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

    # Section 1.2 - Measurement and configuration commands

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

    # Section 1.3 - Calibration Commands

    class Calibration:

        def __init__(self, parent):
            self.parent = parent
            self.electricity = self.Electricity(self)

        class Electricity:
            def __init__(self, parent):
                self.parent = parent

            def start_scan(self, mode: int, function: int, range_: int):
                """
                Start an electrical calibration scan.

                This method initiates a calibration scan for electrical parameters
                based on the specified mode, function, and range.

                Parameters:
                    mode (int): The mode of calibration. Only `0` (active calibration) is supported.
                    function (int): The function type for calibration:
                        - 0: Voltage
                        - 1: Current
                        - 2: Resistance
                        - 3: PRT (Platinum Resistance Thermometer)
                        - 4: Thermistor
                    range_ (int): The range of calibration specific to the function type:
                        - Voltage: 0 (100 mV), 1 (1 V), 2 (10 V), 3 (50 V)
                        - Current: 0 (100 µA), 1 (1 mA), 2 (10 mA), 3 (100 mA)
                        - Resistance: 0 (100 Ω), 1 (1 kΩ), 2 (10 kΩ), 3 (100 kΩ),
                        4 (1 MΩ), 5 (10 MΩ), 6 (100 MΩ)
                        - PRT: 0 (100 Ω), 1 (400 Ω), 2 (4 kΩ)
                        - Thermistor: 0 (0–10 kΩ), 1 (10–100 kΩ), 2 (0.1–1 MΩ)

                Raises:
                    ValueError: If `mode` is not 0, or if invalid parameters are provided.

                Returns:
                    None
                """
                if mode != 0:
                    raise ValueError("Only mode 0 (active calibration) is supported")
                command = f'CALibration:ElECtricity:SCAN {mode},{function},{range_}'
                self.parent.parent.send_command(command)

            def get_scan_data(self) -> dict:
                """
                Retrieve the original data of electrical logging during calibration.

                Command:
                    CALibration:ElECtricity:SCAN?

                Parameters:
                    None

                Returns:
                    dict: A dictionary containing the following keys:
                        - 'exception_code': 4-byte exception code.
                        - 'mode': Mode of calibration (e.g., active calibration).
                        - 'function': Function type (voltage, current, resistance, etc.).
                        - 'range': Calibration range.
                        - 'status': Indicates if data is available (1 for available, 0 otherwise).
                        - 'data': The original value as a float if the status is available, otherwise None.
                """

                response = self.parent.parent.send_command("CALibration:ElECtricity:SCAN?")
                if response:
                    parts = response.split(",")
                    return {
                        "exception_code": parts[0],
                        "mode": parts[1],
                        "function": parts[2],
                        "range": parts[3],
                        "status": parts[4],
                        "data": float(parts[5]) if parts[4] == "1" else None
                    }
                return {}

            def write_calibration_data(self, manufacturer_or_user: str, password: str, channel: int,
                                       function: int, range_: int, unit_id: int, count: int,
                                       points: List[float], values: List[float],
                                       year: int, month: int, day: int):
                """
                Write calibration data to the device.

                Command:
                    CALibration:ElECtricity:DATA <Manufacturer|User>,<password>,<channel>,<function>,<range>,
                                                <unitID>,<count>,<points>,<values>,<year>,<month>,<day>

                Parameters:
                    manufacturer_or_user (str): Specifies factory ("Manufactor") or user calibration ("User").
                    password (str): Password for authentication.
                    channel (int): Channel number for calibration:
                        - 01~02: REF1 and REF2.
                        - 101~110: Inner box channels 01A~10A.
                        - 111~120: Inner box channels 01B~10B.
                        - 201~210: External box 1 channels 01A~10A.
                        - 211~220: External box 1 channels 01B~10B.
                        Similar ranges apply for external boxes 2 and 3.
                    function (int): Function type:
                        - 0: Voltage
                        - 1: Current
                        - 2: Resistance
                        - 3: PRT
                        - 4: Thermistor
                        - 5: CJC
                    range_ (int): Range for the selected function:
                        - Voltage: 0 (100mV), 1 (1V), 2 (10V), 3 (50V)
                        - Current: 0 (100µA), 1 (1mA), 2 (10mA), 3 (100mA)
                        - Resistance: 0 (100Ω), 1 (1kΩ), 2 (10kΩ), 3 (100kΩ), 4 (1MΩ), 5 (10MΩ), 6 (100MΩ)
                        - PRT: 0 (100Ω), 1 (400Ω), 2 (4kΩ)
                        - Thermistor: 0 (0–10kΩ), 1 (10–100kΩ), 2 (0.1–1MΩ)
                    unit_id (int): Unit identifier for the calibration.
                    count (int): Number of calibration points.
                    points (List[float]): Calibration points as a list of floats.
                    values (List[float]): Standard values corresponding to calibration points.
                    year (int): Calibration year.
                    month (int): Calibration month.
                    day (int): Calibration day.

                Raises:
                    ValueError: If the number of `points` and `values` does not match `count`.

                Returns:
                    None
                """
                if len(points) != count or len(values) != count:
                    raise ValueError("Number of points and values must match the count")

                points_str = ",".join(map(str, points))
                values_str = ",".join(map(str, values))

                command = (f'CALibration:ElECtricity:DATA {manufacturer_or_user},{password},'
                           f'{channel},{function},{range_},{unit_id},{count},'
                           f'"{points_str}","{values_str}",{year},{month},{day}')
                self.parent.parent.send_command(command)

            def get_calibration_data(self, manufacturer_or_user: str, password: str, channel: int,
                                      function: int, range_: int) -> dict:
                """
                Retrieve calibration data from the device.

                Command:
                    CALibration:ElECtricity:DATA? <Manufacturer|User>,<password>,<channel>,<function>,<range>

                Parameters:
                    manufacturer_or_user (str): Specifies whether to retrieve factory ("Manufactor") or user calibration ("User").
                    password (str): Password for authentication.
                    channel (int): Channel number for calibration:
                        - 01~02: REF1 and REF2.
                        - 101~110: Inner box channels 01A~10A.
                        - 111~120: Inner box channels 01B~10B.
                        - 201~210: External box 1 channels 01A~10A.
                        - 211~220: External box 1 channels 01B~10B.
                        Similar ranges apply for external boxes 2 and 3.
                    function (int): Function type:
                        - 0: Voltage
                        - 1: Current
                        - 2: Resistance
                        - 3: PRT
                        - 4: Thermistor
                        - 5: CJC
                    range_ (int): Range for the selected function:
                        - Voltage: 0 (100mV), 1 (1V), 2 (10V), 3 (50V)
                        - Current: 0 (100µA), 1 (1mA), 2 (10mA), 3 (100mA)
                        - Resistance: 0 (100Ω), 1 (1kΩ), 2 (10kΩ), 3 (100kΩ), 4 (1MΩ), 5 (10MΩ), 6 (100MΩ)
                        - PRT: 0 (100Ω), 1 (400Ω), 2 (4kΩ)
                        - Thermistor: 0 (0–10kΩ), 1 (10–100kΩ), 2 (0.1–1MΩ)

                Returns:
                    dict: A dictionary containing calibration data with the following keys:
                        - "unit_id": Unit identifier.
                        - "count": Number of calibration points.
                        - "points": List of calibration points.
                        - "values": List of standard values.
                        - "year": Calibration year.
                        - "month": Calibration month.
                        - "day": Calibration day.
                """
                command = f'CALibration:ElECtricity:DATA? {manufacturer_or_user},{password},{channel},{function},{range_}'
                response = self.parent.parent.send_command(command)
                
                if response:
                    parts = response.split(",")
                    return {
                        "unit_id": int(parts[0]),
                        "count": int(parts[1]),
                        "points": [float(x) for x in parts[2].split(" ")],
                        "values": [float(x) for x in parts[3].split(" ")],
                        "year": int(parts[4]),
                        "month": int(parts[5]),
                        "day": int(parts[6])
                    }
                return {}

            def cjcnable(self, enable: bool):
                """
                Enable or disable cold junction calibration.

                Command:
                    CALibration:ELECtricity:CJCenable <enable>

                Parameters:
                    enable (bool): Set to True to enable cold junction calibration or False to disable it.

                Returns:
                    None
                """

                command = f'CALibration:ELECtricity:CJCenable {int(enable)}'
                self.parent.parent.send_command(command)

            def get_cjc_data(self, manufacturer_or_user: str, password: str, location: int, channel: int) -> dict:
                """
                Retrieve cold junction calibration data.

                Command:
                    CALibration:ELECtricity:DATA:CJC? <Manufacturer|User>,<password>,<location>,<channel>

                Parameters:
                    manufacturer_or_user (str): Specifies factory ("Manufactor") or user calibration ("User").
                    password (str): Authentication password.
                    location (int): Calibration location:
                        - 1: Internal wiring
                        - 0: External wiring
                    channel (int): Channel identifier:
                        - 101: Embedded location 01A
                        - Similar format for other channels.

                Returns:
                    dict: A dictionary containing cold junction calibration data with the following keys:
                        - "location": Location type (internal or external).
                        - "channel": Channel identifier.
                        - "data_type": Data type (user or manufacturer).
                        - "validity": Whether the data is valid (1 = valid, 0 = invalid).
                        - "offset": Calibration offset value.
                        - "year": Calibration year.
                        - "month": Calibration month.
                        - "day": Calibration day.
                """
                command = f'CALibration:ELECtricity:DATA:CJC? {manufacturer_or_user},{password},{location},{channel}'
                response = self.parent.parent.send_command(command)

                if response:
                    parts = response.split(",")
                    return {
                        "location": int(parts[0]),
                        "channel": int(parts[1]),
                        "data_type": int(parts[2]),
                        "validity": int(parts[3]),
                        "offset": float(parts[4]),
                        "year": int(parts[5]),
                        "month": int(parts[6]),
                        "day": int(parts[7])
                    }
                return {}

            def write_cjc_data(self, manufacturer_or_user: str, password: str, location: int, channel: int,
                               offset: float, year: int, month: int, day: int):
                """
                Write cold junction calibration data.

                Command:
                    CALibration:ELECtricity:DATA:CJC <Manufacturer|User>,<password>,<location>,<channel>,<offset>,<year>,<month>,<day>

                Parameters:
                    manufacturer_or_user (str): Specifies factory ("Manufactor") or user calibration ("User").
                    password (str): Authentication password.
                    location (int): Calibration location:
                        - 1: Internal wiring
                        - 0: External wiring
                    channel (int): Channel identifier (e.g., 101 for embedded position 01A channel).
                    offset (float): Calibration offset value.
                    year (int): Year of calibration.
                    month (int): Month of calibration.
                    day (int): Day of calibration.

                Returns:
                    None
                """

                command = (f'CALibration:ELECtricity:DATA:CJC {manufacturer_or_user},{password},'
                           f'{location},{channel},{offset},{year},{month},{day}')
                self.parent.parent.send_command(command)

    # Section 1.4 - System Commands

    class System:
        def __init__(self, parent):
            self.parent = parent
            self.communicate = self.Communicate(self)

        # 1.4.1
        def getVersion(self, module: Optional[str] = None) -> dict:
            """
            Retrieve version information for the system or a specific module.

            Command:
                SYSTem:VERSion? [<module>]

            Parameters:
                module (str, optional): The module for which to retrieve version information.
                    Valid options include "APPLication", "ElECtricity:FIRMware", "ElECtricity:HARDware",
                    "OS:FIRMware", "OS:HARDware", "JUNCtion:HARDware", "JUNCtion:FIRMware".
                    If not provided, retrieves general SCIP version information.

            Returns:
                dict: A dictionary containing version information.

            Example:
                {"SCIP": "v1.0", "Application": "v1.2"}
            """
            command = f'SYSTem:VERSion? {module}' if module else 'SYSTem:VERSion?'
            response = self.parent.send_command(command)
            if response:
                return {key_value.split(":")[0]: key_value.split(":")[1] for key_value in response.split(",")}
            return {}

        # 1.4.2
        def get_next_error(self) -> dict:
            """
            Retrieve the next error in the system error queue.

            Command:
                SYSTem:ERRor[:NEXT]?

            Returns:
                dict: A dictionary containing:
                    - "error_code" (int): The error code from the system.
                    - "error_message" (str): A description of the error.

            Raises:
                ValueError: If no error information is returned.
            """
            response = self.parent.send_command("SYSTem:ERRor:NEXT?")
            if response:
                parts = response.split(",")
                return {
                    "error_code": int(parts[0]),
                    "error_message": parts[1].strip()
                }
            raise ValueError("No error information returned.")

        # 1.4.3
        def set_date(self, year: int, month: int, day: int):
            """
            Set the system date.

            Command:
                SYSTem:DATE <year>,<month>,<day>

            Parameters:
                year (int): Year to set.
                month (int): Month to set (1-12).
                day (int): Day to set (1-31).

            Returns:
                None
            """
            command = f"SYSTem:DATE {year},{month},{day}"
            self.parent.send_command(command)

        # 1.4.4
        def get_date(self) -> dict:
            """
            Query the system date.

            Command:
                SYSTem:DATE?

            Parameters:
                None

            Returns:
                dict: A dictionary containing:
                    - "year" (int): Current year.
                    - "month" (int): Current month.
                    - "day" (int): Current day.
            """
            response = self.parent.send_command("SYSTem:DATE?")
            if response:
                parts = response.split(",")
                return {
                    "year": int(parts[0]),
                    "month": int(parts[1]),
                    "day": int(parts[2])
                }
            raise ValueError("No date information returned.")

        # 1.4.5
        def set_time(self, hour: int, minute: int, second: int):
            """
            Set the system time.

            Command:
                SYSTem:TIME <hour>,<minute>,<second>

            Parameters:
                hour (int): Hour to set (0-23).
                minute (int): Minute to set (0-59).
                second (int): Second to set (0-59).

            Returns:
                None
            """
            command = f"SYSTem:TIME {hour},{minute},{second}"
            self.parent.send_command(command)

        # 1.4.6
        def set_local_lock(self, lock: bool):
            """
            Set the local lock-out state of the system.

            Command:
                SYSTem:KLOCk <Boolean>|ON|OFF

            Parameters:
                lock (bool): Set to True to lock the system (ON) or False to unlock it (OFF).

            Returns:
                None
            """
            command = f"SYSTem:KLOCk {int(lock)}"
            self.parent.send_command(command)

        # 1.4.7
        def get_local_lock(self) -> bool:
            """
            Query the local lock-out state of the system.

            Command:
                SYSTem:KLOCk?

            Parameters:
                None

            Returns:
                bool: True if the system is locked (ON), False if unlocked (OFF).
            """
            response = self.parent.send_command("SYSTem:KLOCk?")
            if response:
                return bool(response.strip())
            raise ValueError("No lock state information returned.")
        
        # 1.4.8
        def set_warning_tone(self, enable: bool):
            """
            Set the state of the system's warning tone.

            Command:
                SYSTem:BEEPer:ALARm <Boolean>|ON|OFF

            Parameters:
                enable (bool): Set to True to enable the warning tone (ON) or False to disable it (OFF).

            Returns:
                None
            """
            command = f"SYSTem:BEEPer:ALARm {int(enable)}"
            self.parent.send_command(command)

        # 1.4.9
        def set_keypad_tone(self, enable: bool):
            """
            Set the state of the keypad tone.

            Command:
                SYSTem:BEEPer:TOUCh <Boolean>|ON|OFF

            Parameters:
                enable (bool): Set to True to enable the keypad tone (ON) or False to disable it (OFF).

            Returns:
                None
            """
            command = f"SYSTem:BEEPer:TOUCh {int(enable)}"
            self.parent.send_command(command)

        class Password():
            def __init__(self, parent):
                self.parent = parent

            # 1.4.40
            def setPassword(self, old_password: str, new_password: str, new_password_confirm: str):
                """
                Edit the user password

                Command:
                    SYSTem:PASSword <password>

                Parameters:
                    old_password (str): The old password.
                    new_password (str): The new password.
                    new_password_confirm (str): The new password confirmation.

                Returns:
                    None
                """
                self.parent.send_command(f"SYSTem:PASSword {old_password},{new_password},{new_password_confirm}")

            # 1.4.41
            def getProtection(self) -> bool:
                """
                Query that the protection of sensor bank
                password is opened or not

                Command:
                    SYSTem:PASSword:ENABle:SENSor?
                
                Parameters:
                    None

                Returns:
                    bool: True if the protection of sensor bank password is opened, False if not.
                """
                if response := self.parent.send_command("SYSTem:PASSword:ENABle:SENSor?"):
                    return bool(response.strip())
                raise ValueError("No protection information returned.")
            
            # 1.4.42
            def setProtection(self, enable: bool):
                """
                Set the protection of sensor bank password

                Command:
                    SYSTem:PASSword:ENABle:SENSor <enable>

                Parameters:
                    enable (bool): Set to True to enable the protection of sensor bank password.

                Returns:
                    None
                """
                self.parent.send_command(f"SYSTem:PASSword:ENABle:SENSor {int(enable)}")

        class Communicate:
            def __init__(self, parent):
                self.parent = parent
                self.WLAN = self.WLAN(self)
                self.Ethernet = self.Ethernet(self)
                self.Bluetooth = self.Bluetooth(self)

            class WLAN:
                def __init__(self, parent):
                    self.parent = parent

                # 1.4.10
                def setstate(self, enable: bool):
                    """
                    Set the state of the system's WiFi functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN[:STATe] <Boolean>|ON|OFF

                    Parameters:
                        enable (bool): Set to True to enable WiFi (ON) or False to disable it (OFF).

                    Returns:
                        None
                    """
                    command = f"SYSTem:COMMunicate:SOCKet:WLAN:STATe {int(enable)}"
                    self.parent.send_command(command)

                # 1.4.11
                def getstate(self) -> bool:
                    """
                    Query the state of the system's WiFi functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN[:STATe]?

                    Parameters:
                        None

                    Returns:
                        bool: True if WiFi is enabled (ON), False if disabled (OFF).
                    """
                    response = self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:STATe?")
                    if response:
                        return bool(response.strip())
                    raise ValueError("No WiFi state information returned.")
                
                # 1.4.12
                def set_wlan_ip_address(self, ip_address: str):
                    """
                    Set the IP address for the system's WiFi functionality.

                    Design the IP address of WIFI
                    Before designing the DHCP、IP subset
                    mask and gateway of WIFI, please confirm
                    that the wifi module has been opened and
                    doesn’t connect with any hot spots.

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN:ADDRess <ip_address>

                    Parameters:
                        ip_address (str): The IP address to set.

                    Returns:
                        None
                    """
                    # FIXME: Validate IP address format
                    command = f"SYSTem:COMMunicate:SOCKet:WLAN:ADDRess {ip_address}"
                    self.parent.send_command(command)

                # 1.4.13
                def get_ip_address(self) -> str:
                    """
                    Query the IP address for the system's WiFi functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN:ADDRess?

                    Parameters:
                        None

                    Returns:
                        str: The IP address.
                    """
                    if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:ADDRess?"):
                        return response.strip()
                    raise ValueError("No IP address information returned.")
                
                # 1.4.14
                def set_subnet_mask(self, subnet_mask: str):
                    """
                    Set the subnet mask for the system's WiFi functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN:MASK <subnet_mask>

                    Parameters:
                        subnet_mask (str): The subnet mask to set.

                    Returns:
                        None
                    """
                    if response := self.parent.send_command(f"SYSTem:COMMunicate:SOCKet:WLAN:MASK {subnet_mask}"):
                        return response.strip()
                    raise ValueError("No subnet mask information returned.")

                # 1.4.15
                def get_subnet_mask(self) -> str:
                    """
                    Query the subnet mask for the system's WiFi functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN:MASK?

                    Parameters:
                        None

                    Returns:
                        str: The subnet mask.
                    """
                    if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:MASK?"):
                        return response.strip()
                    raise ValueError("No subnet mask information returned.")
                
                # 1.4.16
                def setGateway(self, IPaddress: str):
                    """
                    Set the gateway for the system's WiFi functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN:GATEway <gateway>

                    Parameters:
                        IPaddress (str): The gateway to set.

                    Returns:
                        None
                    """
                    if response := self.parent.send_command(f"SYSTem:COMMunicate:SOCKet:WLAN:GATEway {IPaddress}"):
                        return response.strip()
                    raise ValueError("No gateway information returned.")
                
                # 1.4.17
                def getGateway(self) -> str:
                    """
                    Query the gateway for the system's WiFi functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN:GATEway?

                    Parameters:
                        None

                    Returns:
                        str: The gateway.
                    """
                    if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:GATEway?"):
                        return response.strip()
                    raise ValueError("No gateway information returned.")
                
                # 1.4.18
                def getMAC(self) -> str:
                    """
                    Query the MAC address for the system's WiFi functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN:MAC?

                    Parameters:
                        None

                    Returns:
                        str: The MAC address.
                    """
                    if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:MAC?"):
                        return response.strip()
                    raise ValueError("No MAC address information returned.")
                
                # 1.4.19
                def setDHCP(self, enable: bool):
                    """
                    Set the DHCP state for the system's WiFi functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN:DHCP <Boolean>|ON|OFF

                    Parameters:
                        enable (bool): Set to True to enable DHCP (ON) or False to disable it (OFF).

                    Returns:
                        None
                    """
                    command = f"SYSTem:COMMunicate:SOCKet:WLAN:DHCP {int(enable)}"
                    self.parent.send_command(command)

                # 1.4.20
                def getDHCP(self) -> bool:
                    """
                    Query the DHCP state for the system's WiFi functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN:DHCP?

                    Parameters:
                        None

                    Returns:
                        bool: True if DHCP is open (1), False if closed (0).
                    """
                    response = self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:DHCP?")
                    if response:
                        return bool(response.strip())
                    raise ValueError("No DHCP state information returned.")
                
                # 1.4.21
                def setSSID(self, ssid: str):
                    """
                    Set the SSID for the system's WiFi functionality.

                    If the parameter is all, the Query will be
                    done and all the Queried SSID names and
                    the ways of encryption will be returned. If
                    the parameter is overlooked, the
                    result will return back to the current
                    connected SSID name and the ways of
                    encryption, if there is no connections or no
                    queried hot spots, please return “

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN:SSID <ssid>

                    Parameters:
                        ssid (str): The SSID to set.

                    Returns:
                        {[“ssid: way of encryption”]}
                    """
                    if response := self.parent.send_command(f"SYSTem:COMMunicate:SOCKet:WLAN:SSID {ssid}"):
                        return response.strip()
                    raise ValueError("No SSID information returned.")
                
                # 1.4.22
                def connect(self, ssid: str, password: str):
                    """
                    Connect to a WiFi network.

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN:CONNect <ssid>,<password>

                    Parameters:
                        ssid (str): hot spot name, the character string with quotation
                        encryptionMode, WEP_OFF, WEP_ON, WEP_AUTO, WPA_PSK, WPA_TKIP, WPA2_PSK, WPA2_AES,CCKM_TKIP, WEP_CKIP, WEP_AUTO_CKIP, CCKM_AES, WPA_PSK_AES, WPA_AES, WPA2_PSK_TKIP, WPA2_TKIP, WAPI_PSK, WAPI_CERT
                        password (str): The password for the WiFi network, the character string with quotation

                    Returns:
                        None
                    """
                    command = f"SYSTem:COMMunicate:SOCKet:WLAN:CONNect {ssid},{password}"
                    self.parent.send_command(command)

                # 1.4.23
                def getConnection(self) -> str:
                    """
                    Query the connection status of the system's WiFi functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN:CONNect?

                    Parameters:
                        None

                    Returns:
                        str: The connection status.
                    """
                    if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:CONNect?"):
                        return response.strip()
                    raise ValueError("No connection information returned.")
                
                # 1.4.24
                def disconnect(self):
                    """
                    Disconnect from the current WiFi network.

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN:DISConnect

                    Parameters:
                        None

                    Returns:
                        None
                    """
                    self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:DISConnect")

                # 1.4.25
                def getDBM(self):
                    """Query signal strength and dBm value of WIFI

                    Command:
                        SYSTem:COMMunicate:SOCKet:WLAN:DBM?

                    Parameters:
                        None

                    Returns:
                        str: The signal strength and dBm value.
                    """
                    if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:DBM?"):
                        return response.strip()
                    raise ValueError("No signal strength information returned.")
                
            class Ethernet:
                def __init__(self, parent):
                    self.parent = parent

                # 1.4.26
                def getDHCP(self) -> bool:
                    """
                    Query the DHCP state for the system's Ethernet functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:ETHernet:DHCP?

                    Parameters:
                        None

                    Returns:
                        bool: True if DHCP is open (1), False if closed (0).
                    """
                    response = self.parent.send_command("SYSTem:COMMunicate:SOCKet:ETHernet:DHCP?")
                    if response:
                        return bool(response.strip())
                    raise ValueError("No DHCP state information returned.")
                
                # 1.4.27
                def setDHCP(self, enable: bool):
                    """
                    Set the DHCP state for the system's Ethernet functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:ETHernet:DHCP <Boolean>|ON|OFF

                    Parameters:
                        enable (bool): Set to True to enable DHCP (ON) or False to disable it (OFF).

                    Returns:
                        None
                    """
                    command = f"SYSTem:COMMunicate:SOCKet:ETHernet:DHCP {int(enable)}"
                    self.parent.send_command(command)

                # 1.4.28
                def getIP(self) -> str:
                    """
                    Query the IP address for the system's Ethernet functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:ETHernet:ADDRess?

                    Parameters:
                        None

                    Returns:
                        str: The IP address.
                    """
                    if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:ETHernet:ADDRess?"):
                        return response.strip()
                    raise ValueError("No IP address information returned.")
                
                # 1.4.29
                def setIP(self, ip_address: str):
                    """
                    Set the IP address for the system's Ethernet functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:ETHernet:ADDRess <ip_address>

                    Parameters:
                        ip_address (str): The IP address to set.

                    Returns:
                        None
                    """
                    if response := self.parent.send_command(f"SYSTem:COMMunicate:SOCKet:ETHernet:ADDRess {ip_address}"):
                        return response.strip()
                    raise ValueError("No IP address information returned.")
                
                # 1.4.30
                def getMASK(self) -> str:
                    """
                    Query the subnet mask for the system's Ethernet functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:ETHernet:MASK?

                    Parameters:
                        None

                    Returns:
                        str: The subnet mask.
                    """
                    if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:ETHernet:MASK?"):
                        return response.strip()
                    raise ValueError("No subnet mask information returned.")
                
                # 1.4.31
                def setMASK(self, subnet_mask: str):
                    """
                    Set the subnet mask for the system's Ethernet functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:ETHernet:MASK <subnet_mask>

                    Parameters:
                        subnet_mask (str): The subnet mask to set.

                    Returns:
                        None
                    """
                    if response := self.parent.send_command(f"SYSTem:COMMunicate:SOCKet:ETHernet:MASK {subnet_mask}"):
                        return response.strip()
                    raise ValueError("No subnet mask information returned.")
                
                # 1.4.32
                def getGATEway(self) -> str:
                    """
                    Query the gateway for the system's Ethernet functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:ETHernet:GATEway?

                    Parameters:
                        None

                    Returns:
                        str: The gateway.
                    """
                    if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:ETHernet:GATEway?"):
                        return response.strip()
                    raise ValueError("No gateway information returned.")
                
                # 1.4.33
                def setGATEway(self, gateway: str):
                    """
                    Set the gateway for the system's Ethernet functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:ETHernet:GATEway <gateway>

                    Parameters:
                        gateway (str): The gateway to set.

                    Returns:
                        None
                    """
                    if response := self.parent.send_command(f"SYSTem:COMMunicate:SOCKet:ETHernet:GATEway {gateway}"):
                        return response.strip()
                    raise ValueError("No gateway information returned.")
                
                # 1.4.34
                def getMAC(self) -> str:
                    """
                    Query the MAC address for the system's Ethernet functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:ETHernet:MAC?

                    Parameters:
                        None

                    Returns:
                        str: The MAC address.
                    """
                    if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:ETHernet:MAC?"):
                        return response.strip()
                    raise ValueError("No MAC address information returned.")
                
                # 1.4.35
                def initialize(self, enable: bool):
                    """
                    Initialize the Ethernet registry.

                    Command:
                        SYSTem:COMMunicate:SOCKet:ETHernet:INITialize

                    Parameters:
                        enable (bool): Set to True to initialize the Ethernet registry.

                    Returns:
                        None
                    """
                    self.parent.send_command(f"SYSTem:COMMunicate:SOCKet:ETHernet:INITialize {int(enable)}")

                # 1.4.36
                def setKey(self, path: str, name: str, keyValue: str, valueType):
                    """
                    Write the key value to the registry.
                    BINary is binary data, and each byte is
                    separated by -, for example, binary data
                    0x11, 0x22, 0xaa, 0xbb, expressed as "11-
                    22-aa-bb";
                    DWord is a 32-bit integer;
                    ExpandString specifies a
                    NULL-terminated string containing an
                    unexpanded reference to an environment
                    variable (such as %PATH%, which
                    expands when the value is
                    retrieved).MultiString is an array of strings,
                    separating each string with -, and a single
                    string needs to be enclosed in
                    parentheses, for
                    example"(abc)-(123er)-(hello,333)"
                    QWord is a 64-bit integer
                    String is a string

                    Command: SYSTem:REGistry:DATA<QuoteStr>,<QuoteStr>,<QuoteStr>,BINary|DWord|ExpandString|MultiString|QWord|String

                    Args:
                        path (str): The path of the key: a quoted string
                        name (str): The name of the key: a quoted string
                        keyValue (str): The value of the key: a quoted string
                        valueType (_type_): Value type

                    Returns:
                        None
                    """
                    self.parent.send_command(f"SYSTem:REGistry:DATA{path},{name},{keyValue},{valueType}")

                # 1.4.37
                def getKey(self, path: str, name: str) -> str:
                    """
                    Read the key value from the registry.

                    Command:
                        SYSTem:REGistry:DATA? <QuoteStr>,<QuoteStr>

                    Parameters:
                        path (str): The path of the key.
                        name (str): The name of the key.

                    Returns:
                        str: The value of the key.
                    """
                    if response := self.parent.send_command(f"SYSTem:REGistry:DATA? {path},{name}"):
                        return response.strip()
                    raise ValueError("No key value information returned.")
                
                # 1.4.38
                def deleteKey(self, path: str, name: str):
                    """
                    Delete the key from the registry.

                    Command:
                        SYSTem:REGistry:DELete<QuoteStr>,<QuoteStr>

                    Parameters:
                        path (str): The path of the key.
                        name (str): The name of the key.

                    Returns:
                        None
                    """
                    self.parent.send_command(f"SYSTem:REGistry:DELete {path},{name}")

                # 1.4.39
                def saveRegistry(self, keyName: str):
                    """
                    Save the registry to the file.

                    Command:
                        SYSTem:REGistry:SAVE HKEY_LOCAL_MACHINE|HKEY_CLASSES_ROOT|HKEY_CURRENT_USER|HKEY_USERS| ALL

                    Parameters:
                        keyName (str): The key name to save.
                    
                    Returns:
                        None
                    """
                    assert(keyName in ["HKEY_LOCAL_MACHINE", "HKEY_CLASSES_ROOT", "HKEY_CURRENT_USER", "HKEY_USERS", "ALL"])
                    self.parent.send_command(f"SYSTem:REGistry:SAVE {keyName}")

            class Bluetooth:
                def __init__(self, parent):
                    self.parent = parent

                # 1.4.43
                def setstate(self, enable: bool):
                    """
                    Set the state of the system's Bluetooth functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:BLUetooth[:STATe] <Boolean>|ON|OFF

                    Parameters:
                        enable (bool): Set to True to enable Bluetooth (ON) or False to disable it (OFF).

                    Returns:
                        None
                    """
                    command = f"SYSTem:COMMunicate:SOCKet:BLUetooth:STATe {int(enable)}"
                    self.parent.send_command(command)

                # 1.4.44
                def getstate(self) -> bool:
                    """
                    Query the state of the system's Bluetooth functionality.

                    Command:
                        SYSTem:COMMunicate:SOCKet:BLUetooth[:STATe]?

                    Parameters:
                        None

                    Returns:
                        bool: True if Bluetooth is enabled (ON), False if disabled (OFF).
                    """
                    response = self.parent.send_command("SYSTem:COMMunicate:SOCKet:BLUetooth:STATe?")
                    if response:
                        return bool(response.strip())
                    raise ValueError("No Bluetooth state information returned.")
                
                # 1.4.45
                def getName(self) -> str:
                    """
                    Query the name of the Bluetooth device.

                    Command:
                        SYSTem:COMMunicate:BLUEtooth:NAMe?

                    Parameters:
                        None

                    Returns:
                        str: The name of the Bluetooth device.
                    """
                    if response := self.parent.send_command("SYSTem:COMMunicate:BLUEtooth:NAMe?"):
                        return response.strip()
                    raise ValueError("No Bluetooth name information returned.")
                    
                # 1.4.46 (SYSTem:COMMunicate:BLUEtooth:NAMe<UnquoStr>))
                def setName(self, name: str):
                    """
                    Set the name of the Bluetooth device.

                    Command:
                        SYSTem:COMMunicate:BLUEtooth:NAMe <UnquoStr>

                    Parameters:
                        name (str): The name to set.

                    Returns:
                        None
                    """
                    self.parent.send_command(f"SYSTem:COMMunicate:BLUEtooth:NAMe {name}")

    # Section 1.5 - Program Commands

    class Program:
        def __init__(self, parent, parameter):
            self.parent = parent

        # 1.5.1
        def run(self, progname: str, parameters: str):
            """Run the appointed program
            
            Command:
                PROGram:RUN <progname>[,<parameters>]
            
            Parameters:
                progname (str): The name of the program to run.
                parameters (str): The parameters of the program.
            """
            self.parent.send_command(f'PROGram:RUN "{progname}" "{parameters}"')

        # 1.5.2
        def exit(self, progname: str = ""):
            """Stop the program. without parameters
                means Stop program specified by
                PROGram:RUN
            
            Command:
                PROGram:EXIT [<progname>]
            """
            self.parent.send_command(f'PROGram:EXIT "{progname}"'.strip())
        
        # 1.5.3
        def state(self, progname: str = "") -> str:
            """Query the state of the program

            Status of interrogator , without
            parameters means to question the
            program specified by PROGram:RUN

            Command:
                PROGram:STATe [<progname>]
            
            Parameters:
                progname (str): The name of the program to query.
            
            Returns:
                str: The state of the program.
            """
            if response := self.parent.send_command(f'PROGram:STATe "{progname}"'):
                return response.strip()
            raise ValueError("No program state information returned.")
        
