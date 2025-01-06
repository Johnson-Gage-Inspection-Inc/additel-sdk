from .channel import DIFunctionChannelConfig
from .DIScanInfo import DIScanInfo as DSI
from .DIModuleInfo import DIModuleInfo as DMI
from .DIReading import DIReading as DR

class DI:
    DIFunctionChannelConfig = DIFunctionChannelConfig
    DIScanInfo = DSI
    DIModuleInfo = DMI
    DIReading = DR

    def __init__(self, parent):
        self.parent = parent
