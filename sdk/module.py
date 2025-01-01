# module.py - Additel Module class
# Description: Contains the Additel Module class with methods for acquiring module information and configuring junction box modules.

# Section 1.2 - Measurement and configuration commands

from typing import List
from customTypes import DIModuleInfo, DIFunctionChannelConfig
import json

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
        if index not in range(5):
            raise ValueError("Module index must be between 0 and 4 inclusive.")
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
        if module_index not in range(5):
            raise ValueError("Module index must be between 0 and 4 inclusive.")
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
