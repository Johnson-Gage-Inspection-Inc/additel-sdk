

from typing import List, Optional
import logging
from dataclasses import dataclass


@dataclass
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
    """

    Index: int  # Identifier of box
    #   (0: front panel, 1: embedded junction box, 2-4: serial-wound junction boxes)
    Category: int  # Module Category type.
    SN: str  # Box serial number
    HwVersion: str  # Hardware version of the module.
    SwVersion: str  # Software version of the module.
    TotalChannelCount: int  # (int): Total number of channels in the module.
    Label: Optional[str] = None  # Optional label for the module.

    @classmethod
    def from_str(cls, string: str) -> List["DIModuleInfo"]:
        # FIXME:  These mappings are not confirmed.
        logging.warning("The mappings for DIModuleInfo.from_str are not confirmed.")
        modules = []
        for mod in string.split(";"):
            if not mod:
                continue
            parts = mod.split(",")
            modules.append(
                cls(
                    Index=int(parts[0]),
                    Category=int(parts[2]),
                    SN=parts[1],
                    HwVersion=parts[3],
                    SwVersion=parts[4],
                    TotalChannelCount=int(parts[5]),
                    Label=parts[6] if len(parts) > 6 else None,
                )
            )
        return modules

    def __str__(s):
        return f"{s.Index},{s.Category},{s.SN},{s.HwVersion},{s.SwVersion},{s.TotalChannelCount},{s.Label};"  # noqa: E501
