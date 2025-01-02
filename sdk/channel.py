# channel.py

from .customTypes import type
import json

class Channel:
    def __init__(self, parent):
        self.parent = parent

    def get_configuration(self, channel_name: str) -> type.DIFunctionChannelConfig:
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
            return type.DIFunctionChannelConfig(**json.loads(response))
        return None

    def configure(self, channel_config: type.DIFunctionChannelConfig):
        """Acquire channel configuration in JSON format.

        This command retrieves configuration data for one or more channels in JSON format.

        Parameters:
            channel_names (type.DIFunctionChannelConfig): A list of channel configurations. Each configuration includes:
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
