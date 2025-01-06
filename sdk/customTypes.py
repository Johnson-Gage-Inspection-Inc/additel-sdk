from .channel import DIFunctionChannelConfig
from .DIScanInfo import DIScanInfo as DSI
from .module import DIModuleInfo
from .DIReading import DIReading as DR

class DI:
    DIFunctionChannelConfig = DIFunctionChannelConfig
    DIScanInfo = DSI
    DIModuleInfo = DIModuleInfo
    DIReading = DR

    def __init__(self, parent):
        self.parent = parent
