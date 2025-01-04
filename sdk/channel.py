# channel.py

from .customTypes import DI
from .coerce import coerce
from typing import List

class Channel:
    def __init__(self, parent):
        self.parent = parent

    valid_names = ['REF1', 'REF2', 'CH1-01A', 'CH1-01B', 'CH1-02A', 'CH1-02B', 'CH1-03A', 'CH1-03B', 'CH1-04A', 'CH1-04B', 'CH1-05A', 'CH1-05B', 'CH1-06A', 'CH1-06B', 'CH1-07A', 'CH1-07B', 'CH1-08A', 'CH1-08B', 'CH1-09A', 'CH1-09B', 'CH1-10A', 'CH1-10B']

    def get_configuration_json(self, channel_names: List[str]) -> List[DI.DIFunctionChannelConfig]:  # Tested!
        """Acquire the configuration of a specific channel.

        This command retrieves the configuration for a specified channel.

        Args:
            channel_names (str): The channels to query.

        Returns:
            List[DI.DIFunctionChannelConfig]:
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
        names_str = ','.join(channel_names)
        assert all(name in self.valid_names for name in channel_names), "Invalid channel name."
        if response := self.parent.cmd(f'CHANnel:CONFig:JSON? "{names_str}"'):
            return coerce(response)

    def get_configuration(self, channel_name: str) -> List[DI.DIFunctionChannelConfig]:  # Tested!
        assert channel_name in self.valid_names, "Invalid channel name."
        if response := self.parent.cmd(f'CHANnel:CONFig? "{channel_name}"'):
            return DI.DIFunctionChannelConfig.from_str(response)

    def configure(self, channel_config: DI.DIFunctionChannelConfig):  # Not yet implemented.
        """Acquire channel configuration in JSON format.

        This command retrieves configuration data for one or more channels in JSON format.

        Args:
            channel_names (DI.DIFunctionChannelConfig): A list of channel configurations. Each configuration includes:
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
        raise NotImplementedError("This function is not implemented yet.")
        command = f'CHANnel:CONFig {channel_config.to_str()}'
        self.parent.cmd(command)

    def set_zero(self, enable: bool):  # Not yet implemented.
        """Enable or disable zero clearing for a single channel.

        This command sets or cancels zero clearing for a specific channel.

        Args:
            enable (int): 1 to enable zero clearing, 0 to cancel.

        Returns:
            None
        """
        raise NotImplementedError("This function is not implemented yet.")
        command = f"CHANnel:ZERo {int(enable)}"
        self.parent.cmd(command)
