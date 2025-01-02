# module.py - Additel Module class
# Description: Contains the Additel Module class with methods for acquiring module information and configuring junction box modules.

# Section 1.2 - Measurement and configuration commands

from typing import List
from .customTypes import DI
import json

class Module:
    def __init__(self, parent):
        self.parent = parent

    # 1.2.1
    def info_str(self) -> List[DI.DIModuleInfo]:
        """Acquire module information.

        This command retrieves information about the front panel and junction box modules.

        Returns:
            List[DIModuleInfo]: A list of parsed module information objects.
        """
        if response := self.parent.send_command("MODule:INFormation?"):
            modules = response.split(';')
            return [
                DI.DIModuleInfo(
                    Index=mod.split(',')[0],
                    Category=mod.split(',')[1],
                    SN=mod.split(',')[2],
                    HwVersion=mod.split(',')[3],
                    SwVersion=mod.split(',')[4],
                    TotalChannelCount=mod.split(',')[5],
                    Label=mod.split(',')[6],
                    ClassName=mod.split(',')[7]
                )
                for mod in modules
            ]
        return []

    # 1.2.2
    def info(self) -> List[DI.DIModuleInfo]:
        """Acquire module information.

        This command retrieves information about the front panel and junction box modules.

        Returns:
            List[DIModuleInfo]: A list of parsed module information objects.
        """
        response = self.parent.send_command("JSON:MODule:INFormation?")
        if response:
            raw_data = json.loads(response)
            modules = raw_data.get('$values', [])
            for mod in modules:
                del mod['$type']
                assert list(mod) == ['Index', 'Category', 'SN', 'HwVersion', 'SwVersion', 'TotalChannelCount', 'Label', 'ClassName'], "Unexpected keys in module info"
            return [DI.DIModuleInfo.from_json(mod) for mod in modules]
        raise ValueError("No module information received")

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
        if index not in range(5):
            raise ValueError("Module index must be between 0 and 4 inclusive.")
        command = f'MODule:LABel {index},"{label}"'
        self.parent.send_command(command)

    # 1.2.4
    def getConfiguration(self, module_index: int) -> List[DI.DIFunctionChannelConfig]:
        """Acquire channel configuration of a specified junction box.

        This command retrieves the channel configuration for a specified junction box module.

        Args:
            module_index (int): The module id (0: Front panel, 1: Embedded junction box, 2, 3, 4: Serial-wound junction boxes)

        Returns:
            List[DI.DIFunctionChannelConfig]: A list of channel configurations for the specified module.
        """
        if module_index not in range(5):
            raise ValueError("Module index must be between 0 and 4 inclusive.")
        response = self.parent.send_command(f"MODule:CONFig? {module_index}")
        if response:
            return [DI.DIFunctionChannelConfig.from_str(config) for config in response.split(';') if config]
            # return [DI.DIFunctionChannelConfig.from_json(config) for config in json.loads(response)['$values']]
            return [type.DIFunctionChannelConfig.from_str(config) for config in response.split(';') if config]
        return []

    # 1.2.5
    def getConfiguration_json(self, module_index: int) -> List[DI.DIFunctionChannelConfig]:
        """Acquire channel configuration of a specified junction box, in JSON format.

        This command retrieves the channel configuration for a specified junction box module.

        Args:
            module_index (int): The module id (0: Front panel, 1: Embedded junction box, 2, 3, 4: Serial-wound junction boxes)

        Returns:
            List[type.DIFunctionChannelConfig]: A list of channel configurations for the specified module.
        """
        # FIXME: For module_index = 0, it's fine, but for module_index = 1, the response is too long and is getting truncated, so the parsing is failing
        assert module_index in range(5), "Module index must be between 0 and 4 inclusive."
        if response := self.parent.send_command(f"JSON:MODule:CONFig? {module_index}"):
            try:
                return [type.DIFunctionChannelConfig.from_json(config) for config in json.loads(response)['$values']]
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON response: {e}")
                print(f"Response length: {len(response)}")
        return []

    def configure(self, module_index: int, params: List[DI.DIFunctionChannelConfig]):
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
