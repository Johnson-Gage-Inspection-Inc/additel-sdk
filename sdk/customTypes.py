from .channel import DIFunctionChannelConfig
from .scan import DIScanInfo, DIReading
from .module import DIModuleInfo

class DI:
    DIFunctionChannelConfig = DIFunctionChannelConfig
    DIScanInfo = DIScanInfo
    DIModuleInfo = DIModuleInfo
    DIReading = DIReading

    def __init__(self, parent):
        self.parent = parent
