# channel.py
from .coerce import coerce
from typing import List

class DIFunctionChannelConfig(dict):
    """
    Base class for channel configuration. Contains common keys:
      - Name: channel name
      - Enabled: whether the channel is enabled
      - Label: channel label
      - ElectricalFunctionType: function type number
      - Range: range index
      - Delay: channel delay
      - IsAutoRange: automatic range setting (1/0)
      - FilteringCount: number of filters
    """
    # Define the order and expected keys for all channels.
    common_keys = ["Name", "Enabled", "Label", "ElectricalFunctionType", "Range", "Delay", "IsAutoRange", "FilteringCount"]

    def __init__(self, **kwargs):
        try:
            self["Name"] = str(kwargs.pop("Name"))
            self["Enabled"] = int(kwargs.pop("Enabled"))
            self["Label"] = str(kwargs.pop("Label"))
            self["ElectricalFunctionType"] = int(kwargs.pop("ElectricalFunctionType"))
            self["Range"] = int(kwargs.pop("Range"))
            self["Delay"] = int(kwargs.pop("Delay"))
            self["IsAutoRange"] = int(kwargs.pop("IsAutoRange"))
            self["FilteringCount"] = int(kwargs.pop("FilteringCount"))
        except KeyError as e:
            raise ValueError("Missing common key: " + str(e))
        self.validate_name(self["Name"])
        # Let the subclass initialize extra keys.
        self._init_extra(kwargs)
        if kwargs:
            raise ValueError("Unexpected keys: " + str(kwargs))
    
    def _init_extra(self, kwargs):
        """
        Subclasses should override this method to extract their extra keys.
        """
        pass

    def validate_name(self, name):
        valid_names = [
            "REF1", "REF2", "CH1-01A", "CH1-01B", "CH1-02A", "CH1-02B",
            "CH1-03A", "CH1-03B", "CH1-04A", "CH1-04B", "CH1-05A", "CH1-05B",
            "CH1-06A", "CH1-06B", "CH1-07A", "CH1-07B", "CH1-08A", "CH1-08B",
            "CH1-09A", "CH1-09B", "CH1-10A", "CH1-10B",
        ]
        if name not in valid_names:
            raise ValueError(f"Invalid channel name: {name}")

    def __str__(self):
        # Use the common keys plus the extra keys (in a fixed order)
        keys_order = self.common_keys + self.extra_key_order()
        return ",".join(str(self.get(k, "")) for k in keys_order)

    def extra_key_order(self):
        """
        Subclasses should override this method to return a list of extra key names in order.
        """
        return []

    @classmethod
    def expected_types(cls):
        # Common types: Name (str), Enabled (int), Label (str), ElectricalFunctionType (int),
        # Range (int), Delay (int), IsAutoRange (int), FilteringCount (int)
        common_types = [str, int, str, int, int, int, int, int]
        return common_types + cls.extra_types()

    @classmethod
    def extra_types(cls):
        """
        Subclasses should override this method to return a list of types for extra keys.
        """
        return []

    @classmethod
    def from_str(cls, data: str):
        """
        Factory method to parse a channel configuration from a comma-separated string.
        If multiple entries are present (separated by semicolons), returns a list.
        """
        if ";" in data:
            parts = data.split(";")
            parts = [p for p in parts if p]  # drop empty parts
            return [cls.from_str(p) for p in parts]
        # Split the data and determine function type from the fourth value.
        values = data.split(",")
        try:
            func_type = int(values[3])
        except Exception:
            raise ValueError("Cannot determine ElectricalFunctionType from data: " + data)
        subclass = function_type_to_class.get(func_type)
        if subclass is None:
            raise ValueError(f"Unsupported ElectricalFunctionType: {func_type}")
        return subclass._from_str(data)

    @classmethod
    def _from_str(cls, data: str):
        # Parse based on the expected order of keys.
        values = data.split(",")
        keys_order = cls.common_keys + cls.extra_key_order()
        if len(values) != len(keys_order):
            raise ValueError(f"Expected {len(keys_order)} values, got {len(values)} in {data}")
        types = cls.expected_types()
        kwargs = {}
        for k, v, t in zip(keys_order, values, types):
            kwargs[k] = t(v) if v != "" else None
        return cls(**kwargs)

# --- Subclass Definitions ---

class DIFunctionVoltageChannelConfig(DIFunctionChannelConfig):
    # func_type 0: Voltage – extra parameter: highImpedance (int)
    extra_keys = ["highImpedance"]

    @classmethod
    def extra_key_order(cls):
        return cls.extra_keys

    @classmethod
    def extra_types(cls):
        return [int]

    def _init_extra(self, kwargs):
        for key in self.extra_keys:
            if key not in kwargs:
                raise ValueError(f"Missing key '{key}' for DIFunctionVoltageChannelConfig")
            self[key] = int(kwargs.pop(key))

class DIFunctionCurrentChannelConfig(DIFunctionChannelConfig):
    # func_type 1: Current – no extra parameters
    extra_keys = []

    @classmethod
    def extra_key_order(cls):
        return cls.extra_keys

    @classmethod
    def extra_types(cls):
        return []

    def _init_extra(self, kwargs):
        pass

class DIFunctionResistanceChannelConfig(DIFunctionChannelConfig):
    # func_type 2: Resistance – extra parameters: Wire (int), IsOpenDetect (int)
    extra_keys = ["Wire", "IsOpenDetect"]

    @classmethod
    def extra_key_order(cls):
        return cls.extra_keys

    @classmethod
    def extra_types(cls):
        return [int, int]

    def _init_extra(self, kwargs):
        for key, t in zip(self.extra_keys, self.extra_types()):
            if key not in kwargs:
                raise ValueError(f"Missing key '{key}' for DIFunctionResistanceChannelConfig")
            self[key] = t(kwargs.pop(key))

class DIFunctionRTDChannelConfig(DIFunctionChannelConfig):
    # func_type 3: RTD – extra parameters: Wire, SensorName, SensorSN, Id, IsSquareRooting2Current, CompensateInterval
    extra_keys = ["Wire", "SensorName", "SensorSN", "Id", "IsSquareRooting2Current", "CompensateInterval"]

    @classmethod
    def extra_key_order(cls):
        return cls.extra_keys

    @classmethod
    def extra_types(cls):
        return [int, str, str, str, int, int]

    def _init_extra(self, kwargs):
        for key, t in zip(self.extra_keys, self.extra_types()):
            if key not in kwargs:
                raise ValueError(f"Missing key '{key}' for DIFunctionRTDChannelConfig")
            self[key] = t(kwargs.pop(key))

class DIFunctionThermistorChannelConfig(DIFunctionChannelConfig):
    # func_type 4: Thermistor – extra parameters: Wire, SensorName, SensorSN, Id
    extra_keys = ["Wire", "SensorName", "SensorSN", "Id"]

    @classmethod
    def extra_key_order(cls):
        return cls.extra_keys

    @classmethod
    def extra_types(cls):
        return [int, str, str, str]

    def _init_extra(self, kwargs):
        for key, t in zip(self.extra_keys, self.extra_types()):
            if key not in kwargs:
                raise ValueError(f"Missing key '{key}' for DIFunctionThermistorChannelConfig")
            self[key] = t(kwargs.pop(key))

class DIFunctionTCChannelConfig(DIFunctionChannelConfig):
    # func_type 100: Thermocouple (TC) – extra: IsOpenDetect, SensorName, SensorSN, Id, CjcType, CJCFixedValue, CjcChannelName
    extra_keys = ["IsOpenDetect", "SensorName", "SensorSN", "Id", "CjcType", "CJCFixedValue", "CjcChannelName"]

    @classmethod
    def extra_key_order(cls):
        return cls.extra_keys

    @classmethod
    def extra_types(cls):
        return [int, str, str, str, int, int, str]

    def _init_extra(self, kwargs):
        for key, t in zip(self.extra_keys, self.extra_types()):
            if key not in kwargs:
                raise ValueError(f"Missing key '{key}' for DIFunctionTCChannelConfig")
            self[key] = t(kwargs.pop(key))

class DIFunctionSwitchChannelConfig(DIFunctionChannelConfig):
    # func_type 101: Switch – not specified in the documentation.
    extra_keys = []

    @classmethod
    def extra_key_order(cls):
        return cls.extra_keys

    @classmethod
    def extra_types(cls):
        return []

    def _init_extra(self, kwargs):
        pass

class DIFunctionSPRTChannelConfig(DIFunctionChannelConfig):
    # func_type 102: SPRT – extra: Wire, SensorName, SensorSN, Id, IsSquareRooting2Current, CompensateInterval
    extra_keys = ["Wire", "SensorName", "SensorSN", "Id", "IsSquareRooting2Current", "CompensateInterval"]

    @classmethod
    def extra_key_order(cls):
        return cls.extra_keys

    @classmethod
    def extra_types(cls):
        return [int, str, str, str, int, int]

    def _init_extra(self, kwargs):
        for key, t in zip(self.extra_keys, self.extra_types()):
            if key not in kwargs:
                raise ValueError(f"Missing key '{key}' for DIFunctionSPRTChannelConfig")
            self[key] = t(kwargs.pop(key))

class DIFunctionVoltageTransmitterChannelConfig(DIFunctionChannelConfig):
    # func_type 103: Voltage Transmitter – extra: Wire, SensorName, SensorSN, Id
    extra_keys = ["Wire", "SensorName", "SensorSN", "Id"]

    @classmethod
    def extra_key_order(cls):
        return cls.extra_keys

    @classmethod
    def extra_types(cls):
        return [int, str, str, str]

    def _init_extra(self, kwargs):
        for key, t in zip(self.extra_keys, self.extra_types()):
            if key not in kwargs:
                raise ValueError(f"Missing key '{key}' for DIFunctionVoltageTransmitterChannelConfig")
            self[key] = t(kwargs.pop(key))

class DIFunctionCurrentTransmitterChannelConfig(DIFunctionChannelConfig):
    # func_type 104: Current Transmitter – extra: Wire, SensorName, SensorSN, Id
    extra_keys = ["Wire", "SensorName", "SensorSN", "Id"]

    @classmethod
    def extra_key_order(cls):
        return cls.extra_keys

    @classmethod
    def extra_types(cls):
        return [int, str, str, str]

    def _init_extra(self, kwargs):
        for key, t in zip(self.extra_keys, self.extra_types()):
            if key not in kwargs:
                raise ValueError(f"Missing key '{key}' for DIFunctionCurrentTransmitterChannelConfig")
            self[key] = t(kwargs.pop(key))

class DIFunctionStandardTCChannelConfig(DIFunctionChannelConfig):
    # func_type 105: Standard TC – extra: IsOpenDetect, SensorName, SensorSN, Id, CjcType, CJCFixedValue, CjcChannelName
    extra_keys = ["IsOpenDetect", "SensorName", "SensorSN", "Id", "CjcType", "CJCFixedValue", "CjcChannelName"]

    @classmethod
    def extra_key_order(cls):
        return cls.extra_keys

    @classmethod
    def extra_types(cls):
        return [int, str, str, str, int, int, str]

    def _init_extra(self, kwargs):
        for key, t in zip(self.extra_keys, self.extra_types()):
            if key not in kwargs:
                raise ValueError(f"Missing key '{key}' for DIFunctionStandardTCChannelConfig")
            self[key] = t(kwargs.pop(key))

class DIFunctionCustomRTDChannelConfig(DIFunctionChannelConfig):
    # func_type 106: Custom RTD – extra: Wire, SensorName, SensorSN, Id, IsSquareRooting2Current, CompensateInterval
    extra_keys = ["Wire", "SensorName", "SensorSN", "Id", "IsSquareRooting2Current", "CompensateInterval"]

    @classmethod
    def extra_key_order(cls):
        return cls.extra_keys

    @classmethod
    def extra_types(cls):
        return [int, str, str, str, int, int]

    def _init_extra(self, kwargs):
        for key, t in zip(self.extra_keys, self.extra_types()):
            if key not in kwargs:
                raise ValueError(f"Missing key '{key}' for DIFunctionCustomRTDChannelConfig")
            self[key] = t(kwargs.pop(key))

class DIFunctionStandardResistanceChannelConfig(DIFunctionChannelConfig):
    # func_type 110: Standard Resistance – not specified in the documentation.
    extra_keys = []

    @classmethod
    def extra_key_order(cls):
        return cls.extra_keys

    @classmethod
    def extra_types(cls):
        return []

    def _init_extra(self, kwargs):
        pass

# Mapping from ElectricalFunctionType to corresponding subclass.
function_type_to_class = {
    0: DIFunctionVoltageChannelConfig,
    1: DIFunctionCurrentChannelConfig,
    2: DIFunctionResistanceChannelConfig,
    3: DIFunctionRTDChannelConfig,
    4: DIFunctionThermistorChannelConfig,
    100: DIFunctionTCChannelConfig,
    101: DIFunctionSwitchChannelConfig,
    102: DIFunctionSPRTChannelConfig,
    103: DIFunctionVoltageTransmitterChannelConfig,
    104: DIFunctionCurrentTransmitterChannelConfig,
    105: DIFunctionStandardTCChannelConfig,
    106: DIFunctionCustomRTDChannelConfig,
    110: DIFunctionStandardResistanceChannelConfig,
}

# --- Channel Command Interface ---

class Channel:
    def __init__(self, parent):
        self.parent = parent

    def get_configuration_json(self, channel_names: List[str]) -> List[DIFunctionChannelConfig]:
        names_str = ",".join(channel_names)
        if response := self.parent.cmd(f'CHANnel:CONFig:JSON? "{names_str}"'):
            return coerce(response)

    def get_configuration(self, channel_name: str) -> List[DIFunctionChannelConfig]:
        if response := self.parent.cmd(f'CHANnel:CONFig? "{channel_name}"'):
            return DIFunctionChannelConfig.from_str(response)

    def configure(self, config: DIFunctionChannelConfig):  # Not yet implemented.
        """Set channel configuration.

        Args:
            config (DIFunctionChannelConfig): A channel configuration object.

        Returns:
            None
        """
        raise NotImplementedError("This function is not implemented yet.")
        command = f"CHANnel:CONFig {config};"
        self.parent.send_command(command)

    def set_zero(self, enable: bool):  # Not yet implemented.
        """Enable or disable zero clearing for a single channel.

        This command sets or cancels zero clearing for a specific channel.

        Args:
            enable (bool): True to enable zero clearing, False to cancel.

        Returns:
            None
        """
        raise NotImplementedError("This function is not implemented yet.")
        command = f"CHANnel:ZERo {int(enable)}"
        self.parent.send_command(command)
