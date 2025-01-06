# module.py - Additel Module class
# Description: Contains the Additel Module class with methods for acquiring module information and configuring junction box modules.

# Section 1.2 - Measurement and configuration commands

from typing import List, Optional
import json
import logging
from .channel import DIFunctionChannelConfig
from .coerce import coerce

class DIModuleInfo(dict):
    """Data structure for module information.

    Identifier of box :The front
    panel is 0. The embedded
    junction box is 1. Then the
    seris-wound junction boxes
    are in 2, 3, 4

    Box type, 0=front panel,
    1=temperature box,
    2=process box
    Box hardware version
    Box software version
    Total number of box channel
    Label of box

    Each configuration includes:
        Index (int): Identifier of box (e.g., 0: front panel, 1: embedded junction box, 2-4: serial-wound junction boxes).
        Category (int): Module Category type.
        SN (str): Box serial number
        HwVersion (str): Hardware version of the module.
        SwVersion (str): Software version of the module.
        TotalChannelCount (int): Total number of channels in the module.
        Label (Optional[str]): Optional label for the module.
        ClassName (Optional[str]): Class name of the module (if provided).
    """
    def __init__(self,
                 Index: int,
                 Category: int,
                 SN: str,
                 HwVersion: str,
                 SwVersion: str,
                 TotalChannelCount: int,
                 Label: Optional[str] = None):
        self['Index'] = int(Index)  # Identifier of the module
        self['Category'] = int(Category)  # Box type (0: front panel, 1: temperature box, 2: process box)
        self['SN'] = str(SN)  # Serial number of the module
        self['HwVersion'] = str(HwVersion)  # Hardware version
        self['SwVersion'] = str(SwVersion)  # Software version
        self['TotalChannelCount'] = int(TotalChannelCount)  # Total number of channels
        self['Label'] = str(Label) if Label else None  # Optional label

    @classmethod
    def from_str(self, string):
        # FIXME:  These mappings are not confirmed.
        logging.warning("The mappings for DIModuleInfo.from_str are not confirmed.")
        return [
            self(
                Index=mod.split(',')[0],
                Category=mod.split(',')[2],
                SN=mod.split(',')[1],
                HwVersion=mod.split(',')[3],
                SwVersion=mod.split(',')[4],
                TotalChannelCount=mod.split(',')[5],
                Label=mod.split(',')[6]
            )
            for mod in string.split(';')
            if mod
        ]

    @classmethod
    def __str__(self):
        return f"{self['Index']},{self['Category']},{self['SN']},{self['HwVersion']},{self['SwVersion']},{self['TotalChannelCount']},{self['Label']};"

class Module:
    def __init__(self, parent):
        self.parent = parent

    # 1.2.1
    def info_str(self) -> List[DIModuleInfo]:  # Tested!
        """Acquire module information.

        This command retrieves information about the front panel and junction box modules.

        Returns:
            List[DIModuleInfo]: A list of parsed module information objects.
        """
        if response := self.parent.cmd("MODule:INFormation?"):
            return DIModuleInfo.from_str(response)  # NOTE: Can't coerce here, because the response doesn't indicate the type
        return []

    # 1.2.2
    def info(self) -> List[DIModuleInfo]:  # Tested!
        """Acquire module information.

        This command retrieves information about the front panel and junction box modules.

        Returns:
            List[DIModuleInfo]: A list of parsed module information objects.
        """
        if response := self.parent.cmd("JSON:MODule:INFormation?"):
            raw_data = json.loads(response)
            modules = raw_data.get('$values', [])
            for mod in modules:
                assert list(mod) == ['$type', 'Index', 'Category', 'SN', 'HwVersion', 'SwVersion', 'TotalChannelCount', 'Label', 'ClassName'], "Unexpected keys in module info"
            return coerce(modules)
        raise ValueError("No module information received")

    def set_label(self, index: int, label: str):  # Not yet implemented
        """Set the label of a specific junction box module.

        This command assigns a custom label to a specified module.

        Args:
            index (int): The identifier of the junction box. Values:
                - 0: Front panel
                - 1: Embedded junction box
                - 2, 3, 4: Serial-wound junction boxes
            label (str): The label to assign to the module (enclosed in quotation marks).

        Returns:
            None
        """
        raise NotImplementedError("This method is not yet implemented.")
        if index not in range(5):
            raise ValueError("Module index must be between 0 and 4 inclusive.")
        command = f'MODule:LABel {index},"{label}"'
        self.parent.cmd(command)

    # 1.2.4
    def getConfiguration(self, module_index: int) -> List[DIFunctionChannelConfig]:  # Tested!
        """Acquire channel configuration of a specified junction box.

        This command retrieves the channel configuration for a specified junction box module.

        Args:
            module_index (int): The module id (0: Front panel, 1: Embedded junction box, 2, 3, 4: Serial-wound junction boxes)

        Returns:
            List[DIFunctionChannelConfig]: A list of channel configurations for the specified module.
        """
        if module_index not in range(5):
            raise ValueError("Module index must be between 0 and 4 inclusive.")
        if response := self.parent.cmd(f"MODule:CONFig? {module_index}"):
            array = response.split(';')
            if not array[-1]:
                array.pop()
            for string in array:
                rebuilt_str = str(DIFunctionChannelConfig.from_str(string))
                assert string == rebuilt_str, f"Unexpected response: {string}\nExpected: {rebuilt_str}"
            return DIFunctionChannelConfig.from_str(response)

    # 1.2.5
    def getConfiguration_json(self, module_index: int) -> List[DIFunctionChannelConfig]:  # Tested!
        """Acquire channel configuration of a specified junction box, in JSON format.

        This command retrieves the channel configuration for a specified junction box module.

        Args:
            module_index (int): The module id (0: Front panel, 1: Embedded junction box, 2, 3, 4: Serial-wound junction boxes)

        Returns:
            List[type.DIFunctionChannelConfig]: A list of channel configurations for the specified module.
        """
        if module_index not in range(5):
            raise ValueError("Module index must be between 0 and 4 inclusive.")
        if module_index != 0:
            raise Exception("This method is not effective for module_index != 0. Please use the getConfiguration method instead.")

        if response := self.parent.cmd(f"JSON:MODule:CONFig? {module_index}"):
            try:
                return coerce(response)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON response: {e}")
                print(f"Response length: {len(response)}")
        raise ValueError("No channel configuration received")

    def configure(self, module_index: int, params: List[DIFunctionChannelConfig]):  # Not yet implemented
        """Set the channel configuration of a specified junction box in JSON format.

        This command configures the channel settings for a specified module using JSON.

        Args:
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
        raise NotImplementedError("This method is not yet implemented.")
        # Validate parameters
        if not isinstance(module_index, int):
            raise TypeError(f"Invalid parameter type: {type(module_index)}. Expected int.")
        if not isinstance(params, List):
            raise TypeError(f"Invalid parameter type: {type(params)}. Expected List.")
        for param in params:
            if not isinstance(param, DIFunctionChannelConfig):
                raise TypeError(f"Invalid parameter type: List[{type(param)}]. List[Expected DIFunctionChannelConfig].")

        # Send the command
        json_params = json.dumps([param.__dict__ for param in params])
        self.parent.cmd(f'JSON:MODule:CONFig {module_index},{json_params}')
