# DIModuleInfo.py
from typing import Optional

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
        self.Index = int(Index)  # Identifier of the module
        self.Category = int(Category)  # Box type (0: front panel, 1: temperature box, 2: process box)
        self.SN = str(SN)  # Serial number of the module
        self.HwVersion = str(HwVersion)  # Hardware version
        self.SwVersion = str(SwVersion)  # Software version
        self.TotalChannelCount = int(TotalChannelCount)  # Total number of channels
        self.Label = str(Label)  # Optional label for the module

    @classmethod
    def from_json(self, data: dict):
        """Create a DIModuleInfo object from a JSON object.

        Args:
            data (dict): A dictionary containing the module information.

        Returns:
            DIModuleInfo: An instance of DIModuleInfo populated with the JSON data.
        """
        if isinstance(data, dict):
            assert data['ClassName'] == 'DIModuleInfo', f"Class name mismatch: {data['ClassName']}"
            return self(
                Index=data['Index'],
                Category=data['Category'],
                SN=data['SN'],
                HwVersion=data['HwVersion'],
                SwVersion=data['SwVersion'],
                TotalChannelCount=data['TotalChannelCount'],
                Label=data['Label']
            )
        raise NotImplementedError(f"Invalid data type for DIModuleInfo.from_json: {type(data)}")

    def to_json(self) -> dict:
        """Return a JSON representation of the module information.

        Returns:
            dict: A dictionary containing the module information.
        """
        return {
            'ClassName': 'DIModuleInfo',
            'Index': self.Index,
            'Category': self.Category,
            'SN': self.SN,
            'HwVersion': self.HwVersion,
            'SwVersion': self.SwVersion,
            'TotalChannelCount': self.TotalChannelCount,
            'Label': self.Label
        }

    def __repr__(self):
        return str(self.to_json())

    @classmethod
    def from_str(self, string):
        # FIXME:  These mappings are not confirmed.
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

    def to_str(self):
        return '";'.join([
            f"{self.Index},{self.Category},{self.SN},{self.HwVersion},{self.SwVersion},{self.TotalChannelCount},{self.Label}"
        ]) + ';"'

    @classmethod
    def __str__(self):
        return self.to_str()

    @classmethod
    def keys(self):
        return self.to_json().keys()
