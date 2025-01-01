from typing import List, Optional

class DIModuleInfo:
    """Data structure for module information."""
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
    """Data structure for function channel configuration."""
    def __init__(self, 
                 channel_name: str, 
                 enabled: bool, 
                 label: Optional[str], 
                 function_type: int, 
                 range_index: int, 
                 delay: int, 
                 auto_range: bool, 
                 filters: int, 
                 additional_params: Optional[dict] = None):
        self.channel_name = channel_name  # Name of the channel
        self.enabled = enabled  # Whether the channel is enabled
        self.label = label  # Optional label for the channel
        self.function_type = function_type  # Function type (e.g., 0: voltage, 1: current)
        self.range_index = range_index  # Range index for the channel
        self.delay = delay  # Delay for the channel
        self.auto_range = auto_range  # Whether auto-ranging is enabled
        self.filters = filters  # Number of filters applied
        self.additional_params = additional_params  # Additional parameters based on function type

class DIScanInfo:
    """Data structure for scanning information."""
    def __init__(self, 
                 nplc: int, 
                 sampling_frequency: int, 
                 channels: List[str]):
        self.nplc = nplc  # Number of Power Line Cycles (NPLC)
        self.sampling_frequency = sampling_frequency  # Sampling frequency cycle
        self.channels = channels  # List of channels being scanned
