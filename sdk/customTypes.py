from typing import List, Optional

class DIModuleInfo:
    """Data structure for module information.

    Each configuration includes:
        identifier (int): Identifier of the module.
        serial_number (str): Serial number of the module.
        module_type (int): Module type.
        hardware_version (str): Hardware version of the module.
        software_version (str): Software version of the module.
        total_channels (int): Total number of channels in the module.
        label (str): Optional label for the module.
    """
    def __init__(self, 
                 identifier: int, 
                 serial_number: str, 
                 box_type: int, 
                 hardware_version: str, 
                 software_version: str, 
                 total_channels: int, 
                 label: Optional[str] = None):
        self.identifier = identifier  # Identifier of the box (0: front panel, 1: embedded, etc.)
        self.serial_number = serial_number  # Serial number of the box
        self.box_type = box_type  # Box type (e.g., 0: front panel, 1: temperature box)
        self.hardware_version = hardware_version  # Hardware version of the box
        self.software_version = software_version  # Software version of the box
        self.total_channels = total_channels  # Total number of channels in the box
        self.label = label  # Optional label for the box

class DIFunctionChannelConfig:
    """Data structure for function channel configuration.
    
    Was a semicolon-separated string where each entry represents a channel's configuration.

    Each configuration includes:
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
            """
    def __init__(self, 
                 channel_name: str, 
                 enabled: bool, 
                 label: Optional[str], 
                 func_type: int, 
                 range_index: int, 
                 delay: int, 
                 auto_range: bool, 
                 filters: int, 
                 additional_params: Optional[dict] = None):
        self.channel_name = channel_name  # Name of the channel
        self.enabled = enabled  # Whether the channel is enabled
        self.label = label  # Optional label for the channel
        self.func_type = func_type  # Function type (e.g., 0: voltage, 1: current)
        self.range_index = range_index  # Range index for the channel
        self.delay = delay  # Delay for the channel
        self.auto_range = auto_range  # Whether auto-ranging is enabled
        self.filters = filters  # Number of filters applied
        self.additional_params = additional_params  # Additional parameters based on function type

class DIScanInfo:
    """Data structure for scanning information.

    Each configuration includes:
        nplc (int): Number of Power Line Cycles (NPLC).
        sampling_frequency (int): Sampling frequency cycle.
        channels (List[str]): List of channels being scanned.
    """
    def __init__(self, 
                 nplc: int, 
                 sampling_frequency: int, 
                 channels: List[str]):
        self.nplc = nplc  # Number of Power Line Cycles (NPLC)
        self.sampling_frequency = sampling_frequency  # Sampling frequency cycle
        self.channels = channels  # List of channels being scanned
