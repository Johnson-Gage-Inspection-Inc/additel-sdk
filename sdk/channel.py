# channel.py

from .customTypes import DI
from .coerce import coerce
from typing import List

class Channel:
    def __init__(self, parent):
        self.parent = parent

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
        if response := self.parent.cmd(f'CHANnel:CONFig:JSON? "{names_str}"'):
            return coerce(response)

    def get_configuration(self, channel_name: str) -> List[DI.DIFunctionChannelConfig]:  # Tested!
        if response := self.parent.cmd(f'CHANnel:CONFig? "{channel_name}"'):
            return DI.DIFunctionChannelConfig.from_str(response)

    def configure(self, config: DI.DIFunctionChannelConfig):  # Not yet implemented.
        """Set channel configuration.

        Args:
            config (DI.DIFunctionChannelConfig): A channel configuration object.

        Returns:
            None
        """
        raise NotImplementedError("This function is not implemented yet.")
        command = f"CHANnel:CONFig {config};"
        self.parent.cmd(command)

    def set_zero(self, enable: bool):  # Not yet implemented.
        """Enable or disable zero clearing for a single channel.

        This command sets or cancels zero clearing for a specific channel.

        Args:
            enable (bool): True to enable zero clearing, False to cancel.

        Returns:
            None
        """
        raise NotImplementedError("This function is not implemented yet.")
        command = f"CHANnel:ZERo {int(enable)}"
        self.parent.cmd(command)
