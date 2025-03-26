# module.py - Additel Module class
# Description: Contains the Additel Module class with methods for acquiring module
#   information and configuring junction box modules.

# Section 1.2 - Measurement and configuration commands

from typing import List
import json
from .channel import DI
from .coerce import coerce
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.additel_sdk import Additel



class Module:
    def __init__(self, parent: "Additel"):
        self.parent = parent

    # 1.2.1
    def info_str(self) -> List[DI.DIModuleInfo]:
        """Acquire module information.

        This command retrieves info about the front panel and junction box modules.

        Returns:
            List[DI.DIModuleInfo]: A list of parsed module information objects.
        """
        if response := self.parent.cmd("MODule:INFormation?"):
            return DI.DIModuleInfo.from_str(
                response
            )  # NOTE: Can't coerce here, because the response doesn't indicate the type
        return []

    # 1.2.2
    def info(self) -> List[DI.DIModuleInfo]:
        """Acquire module information.

        This command retrieves info about the front panel and junction box modules.

        Returns:
            List[DI.DIModuleInfo]: A list of parsed module information objects.
        """
        if response := self.parent.cmd("JSON:MODule:INFormation?"):
            raw_data = json.loads(response)
            modules = raw_data.get("$values", [])
            for mod in modules:
                assert list(mod) == [
                    "$type",
                    "Index",
                    "Category",
                    "SN",
                    "HwVersion",
                    "SwVersion",
                    "TotalChannelCount",
                    "Label",
                    "ClassName",
                ], "Unexpected keys in module info"
            return coerce(modules)
        raise ValueError("No module information received")

    def set_label(self, index: int, label: str) -> None:
        """Set the label of a specific junction box module.

        This command assigns a custom label to a specified module.

        Args:
            index (int): The identifier of the junction box. Values:
                - 0: Front panel
                - 1: Embedded junction box
                - 2, 3, 4: Serial-wound junction boxes
            label (str): The label to assign to the module (enclosed in quotation marks)
        """
        raise NotImplementedError("This method is not yet implemented.")
        if index not in range(5):
            raise ValueError("Module index must be between 0 and 4 inclusive.")
        command = f'MODule:LABel {index},"{label}"'
        self.parent.cmd(command)

    # 1.2.4
    def getConfiguration(self, module_index: int) -> List[DI.DIFunctionChannelConfig]:
        """Acquire channel configuration of a specified junction box.

        This command retrieves the channel configuration for a specified junction box
        module.

        Args:
            module_index (int): The module id
            - 0: Front panel
            - 1: Embedded junction box
            - 2, 3, 4: Serial-wound junction boxes

        Returns:
            List[DI.DIFunctionChannelConfig]: A list of channel configurations for the
            specified module.
        """
        if module_index not in range(5):
            raise ValueError("Module index must be between 0 and 4 inclusive.")
        if response := self.parent.cmd(f"MODule:CONFig? {module_index}"):
            return DI.DIFunctionChannelConfig.from_str(response)

    # 1.2.5
    def getConfiguration_json(self, module_index: int) -> List[DI.DIFunctionChannelConfig]:
        """Acquire channel configuration of a specified junction box, in JSON format.

        This command retrieves the channel configuration for a specified junction box
        module.

        Args:
            module_index (int): The module id
            - 0: Front panel
            - 1: Embedded junction box
            - 2, 3, 4: Serial-wound junction boxes

        Returns:
            List[type.DI.DIFunctionChannelConfig]: A list of channel configurations for the
            specified module.
        """
        if module_index not in range(5):
            raise ValueError("Module index must be between 0 and 4 inclusive.")
        if module_index != 0:
            raise ValueError(
                "Only the front panel module can be queried in JSON format. "
                "Use the getConfiguration method instead."
            )
        if response := self.parent.cmd(f"JSON:MODule:CONFig? {module_index}"):
            return coerce(response)
        raise ValueError("No channel configuration received")

    def configure(
        self, module_index: int, params: List[DI.DIFunctionChannelConfig]
    ):  # Not yet implemented
        """Set the channel configuration of a specified junction box in JSON format.

        This command configures the channel settings for a specified module using JSON.

        Args:
            module_index (int): The identifier of the module to configure. Values:
                - 0: Front panel
                - 1: Embedded junction box
                - 2, 3, 4: Serial-wound junction boxes
            params (List[DI.DIFunctionChannelConfig]): A list of channel configurations for
              the specified module.

        Returns:
            dict: The JSON response from the device confirming the configuration.
        """
        raise NotImplementedError("This method is not yet implemented.")
        # Validate parameters
        if module_index not in range(5):
            raise ValueError("Module index must be between 0 and 4 inclusive.")
        if not isinstance(params, List):
            raise TypeError(f"Invalid parameter type: {type(params)}. Expected List.")
        for param in params:
            if not isinstance(param, DI.DIFunctionChannelConfig):
                raise TypeError(
                    f"Invalid parameter type: List[{type(param)}]. "
                    "List[Expected DI.DIFunctionChannelConfig]."
                )

        # Send the command
        json_params = json.dumps([param.__dict__ for param in params])
        self.parent.cmd(f"JSON:MODule:CONFig {module_index},{json_params}")
