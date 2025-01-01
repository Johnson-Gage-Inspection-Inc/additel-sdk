# commmunicate.py

from .wlan import WLAN
from .ethernet import Ethernet
from .bluetooth import Bluetooth

class Communicate:
    def __init__(self, parent):
        self.parent = parent
        self.WLAN = WLAN(self)
        self.Ethernet = Ethernet(self)
        self.Bluetooth = Bluetooth(self)