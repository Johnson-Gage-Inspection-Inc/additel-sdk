from typing import List, TYPE_CHECKING
from ..coerce import coerce
from .DI import DIFunctionChannelConfig
if TYPE_CHECKING:
    from src.additel_sdk import Additel


class Channel:
    valid_names = [
        "REF1", "REF2",
        "CH1-01A","CH1-01B","CH1-02A","CH1-02B",
        "CH1-03A","CH1-03B","CH1-04A","CH1-04B",
        "CH1-05A","CH1-05B","CH1-06A","CH1-06B",
        "CH1-07A","CH1-07B","CH1-08A","CH1-08B",
        "CH1-09A","CH1-09B","CH1-10A","CH1-10B",
    ]

    def __init__(self, parent: "Additel"):
        self.parent = parent

    @classmethod
    def validate_name(cls, name):
        if name not in cls.valid_names:
            raise ValueError(f"Invalid channel name: {name}")

    def get_configuration_json(
        self, channel_names: List[str]
    ) -> List[DIFunctionChannelConfig]:
        for name in channel_names:
            self.validate_name(name)
        names_str = ",".join(channel_names)
        if response := self.parent.cmd(f'CHANnel:CONFig:JSON? "{names_str}"'):
            return coerce(response)

    def get_configuration(self, channel_name: str) -> List[DIFunctionChannelConfig]:
        self.validate_name(channel_name)
        if response := self.parent.cmd(f'CHANnel:CONFig? "{channel_name}"'):
            return DIFunctionChannelConfig.from_str(response)

    def configure(self, config: DIFunctionChannelConfig) -> None:
        """Set channel configuration.

        Args:
            config (DIFunctionChannelConfig): A channel configuration object.
        """
        raise NotImplementedError("This function is not implemented yet.")
        command = f"CHANnel:CONFig {config};"
        self.parent.send_command(command)

    def set_zero(self, enable: bool) -> None:
        """Enable or disable zero clearing for a single channel.

        This command sets or cancels zero clearing for a specific channel.

        Args:
            enable (bool): True to enable zero clearing, False to cancel.
        """
        raise NotImplementedError("This function is not implemented yet.")
        command = f"CHANnel:ZERo {int(enable)}"
        self.parent.send_command(command)
