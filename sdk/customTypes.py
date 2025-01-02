from typing import List, Optional
from .DIFunctionChannelConfig import DIFunctionChannelConfig as FCC

class DI:
    DIFunctionChannelConfig = FCC

    def __init__(self, parent):
        self.parent = parent

    class DIModuleInfo:
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
            self.Index = Index  # Identifier of the module
            self.Category = Category  # Box type (0: front panel, 1: temperature box, 2: process box)
            self.SN = SN  # Serial number of the module
            self.HwVersion = HwVersion  # Hardware version
            self.SwVersion = SwVersion  # Software version
            self.TotalChannelCount = TotalChannelCount  # Total number of channels
            self.Label = Label  # Optional label for the module

        @classmethod
        def from_json(cls, data: dict):
            """Create a DIModuleInfo object from a JSON object.

            Parameters:
                data (dict): A dictionary containing the module information.

            Returns:
                DIModuleInfo: An instance of DIModuleInfo populated with the JSON data.
            """
            if isinstance(data, dict):
                assert data['ClassName'] == 'DIModuleInfo', f"Class name mismatch: {data['ClassName']}"
                return cls(
                    Index=data['Index'],
                    Category=data['Category'],
                    SN=data['SN'],
                    HwVersion=data['HwVersion'],
                    SwVersion=data['SwVersion'],
                    TotalChannelCount=data['TotalChannelCount'],
                    Label=data['Label']
                )
            raise NotImplementedError(f"Invalid data type for DIModuleInfo.from_json: {type(data)}")

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
