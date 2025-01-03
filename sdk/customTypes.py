from .DIFunctionChannelConfig import DIFunctionChannelConfig as DFCC
from .DIScanInfo import DIScanInfo as DSI
from .DIModuleInfo import DIModuleInfo as DMI
from .DIReading import DIReading as DR

class DI:
    DIFunctionChannelConfig = DFCC
    DIScanInfo = DSI
    DIModuleInfo = DMI
    DIReading = DR

    def __init__(self, parent):
        self.parent = parent
