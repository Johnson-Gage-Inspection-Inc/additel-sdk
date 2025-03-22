# commmunicate.py

from .wlan import WLAN
from .ethernet import Ethernet
from .bluetooth import Bluetooth
from re import compile
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.additel_sdk.system import System


class Communicate:
    def __init__(self, parent: "System"):
        self.parent: "System" = parent
        self.WLAN = WLAN(self)
        self.Ethernet = Ethernet(self)
        self.Bluetooth = Bluetooth(self)

    def validate_ip(self, ip_address: str) -> None:
        pattern = compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if not pattern.match(ip_address):
            raise ValueError("Invalid IP address format.")