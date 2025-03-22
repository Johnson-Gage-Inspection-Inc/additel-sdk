# calibration.py

from .electricity import Electricity


class Calibration:

    def __init__(self, parent):
        self.parent = parent
        self.electricity = Electricity(self)
