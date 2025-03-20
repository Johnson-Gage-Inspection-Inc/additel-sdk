# channel.py
from .coerce import coerce
from typing import List


class DIFunctionChannelConfig:
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

    common_keys = [
        "Name",
        "Enabled",
        "Label",
        "ElectricalFunctionType",
        "Range",
        "Delay",
        "IsAutoRange",
        "FilteringCount"
    ]

    def __init__(cls, **kwargs):
        try:
            cls.Name = str(kwargs.pop("Name"))
            cls.Enabled = int(kwargs.pop("Enabled"))
            cls.Label = str(kwargs.pop("Label", ""))
            cls.ElectricalFunctionType = int(kwargs.pop("ElectricalFunctionType"))
            cls.Range = int(kwargs.pop("Range"))
            cls.Delay = int(kwargs.pop("Delay"))
            cls.IsAutoRange = int(kwargs.pop("IsAutoRange"))
            cls.FilteringCount = int(kwargs.pop("FilteringCount"))
        except KeyError as e:
            raise ValueError("Missing common key: " + str(e))

        cls.__dict__.update(kwargs)  # Handle additional keys dynamically

    def __repr__(cls):
        return cls.__str__()

    def __str__(cls):
        # Use the common keys plus the extra keys (in a fixed order)
        keys_order = cls.get_keys_order()
        return ",".join(str(cls.__dict__.get(k, "")) for k in keys_order)

    def _addSubclassAttributes(cls, kwargs):
        for key in cls.extra_keys:
            if key in kwargs:
                setattr(cls, key, kwargs.pop(key))
            # else:
            #     raise ValueError(f"Missing key '{key}' for {cls.__class__.__name__}")

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
            raise ValueError(
                "Cannot determine ElectricalFunctionType from data: " + data
            )
        subclass = getSubclass(func_type)
        if subclass is None:
            raise ValueError(f"Unsupported ElectricalFunctionType: {func_type}")
        return subclass._from_str(data)

    @classmethod
    def _from_str(cls, data: str):
        # Parse based on the expected order of keys.
        values = data.split(",")
        keys_order = cls.get_keys_order()
        # if len(values) != len(keys_order):
        #     raise ValueError(
        #         f"Expected {len(keys_order)} values, got {len(values)} in {data}"
        #     )
        types = cls.expected_types()
        kwargs = {}
        for k, v, t in zip(keys_order, values, types):
            kwargs[k] = t(v) if v != "" else None
        return cls(**kwargs)

    @classmethod
    def get_keys_order(cls):
        keys_order = [
            "Name",
            "Enabled",
            "Label",
            "ElectricalFunctionType",
            "Range",
            "Delay",
            "IsAutoRange",
            "FilteringCount"
        ]
        if hasattr(cls, "extra_keys"):
            keys_order += cls.extra_keys
        return keys_order


# --- Subclass Definitions ---


class DIFunctionVoltageChannelConfig(DIFunctionChannelConfig):
    """Voltage Function Channel Configuration"""

    extra_keys = ["highImpedance"]

    def __init__(cls, **kwargs):
        cls._addSubclassAttributes(kwargs)

        super().__init__(**kwargs)


class DIFunctionCurrentChannelConfig(DIFunctionChannelConfig):
    # func_type 1: Current – no extra parameters
    extra_keys = []

    def __init__(cls, **kwargs):
        cls._addSubclassAttributes(kwargs)

        super().__init__(**kwargs)


class DIFunctionResistanceChannelConfig(DIFunctionChannelConfig):
    # func_type 2: Resistance – extra parameters: Wire (int), IsOpenDetect (int)
    extra_keys = ["Wire", "IsOpenDetect"]

    def __init__(cls, **kwargs):
        cls._addSubclassAttributes(kwargs)

        super().__init__(**kwargs)


class DIFunctionRTDChannelConfig(DIFunctionChannelConfig):
    # func_type 3: RTD – extra parameters: Wire, SensorName, SensorSN, Id, IsSquareRooting2Current, CompensateInterval
    extra_keys = [
        "Wire",
        "SensorName",
        "SensorSN",
        "Id",
        "IsSquareRooting2Current",
        "CompensateInterval",
    ]

    def __init__(cls, **kwargs):
        cls._addSubclassAttributes(kwargs)

        super().__init__(**kwargs)


class DIFunctionThermistorChannelConfig(DIFunctionChannelConfig):
    # func_type 4: Thermistor – extra parameters: Wire, SensorName, SensorSN, Id
    extra_keys = ["Wire", "SensorName", "SensorSN", "Id"]

    def __init__(cls, **kwargs):
        cls._addSubclassAttributes(kwargs)

        super().__init__(**kwargs)


class DIFunctionTCChannelConfig(DIFunctionChannelConfig):
    # func_type 100: Thermocouple (TC) – extra: IsOpenDetect, SensorName, SensorSN, Id, CjcType, CJCFixedValue, CjcChannelName
    extra_keys = [
        "IsOpenDetect",
        "SensorName",
        "SensorSN",
        "Id",
        "CjcType",
        "CJCFixedValue",
        "CjcChannelName",
    ]

    def __init__(cls, **kwargs):
        cls._addSubclassAttributes(kwargs)

        super().__init__(**kwargs)


class DIFunctionSwitchChannelConfig(DIFunctionChannelConfig):
    # func_type 101: Switch – not specified in the documentation.
    extra_keys = []

    def __init__(cls, **kwargs):
        cls._addSubclassAttributes(kwargs)

        super().__init__(**kwargs)


class DIFunctionSPRTChannelConfig(DIFunctionChannelConfig):
    # func_type 102: SPRT – extra: Wire, SensorName, SensorSN, Id, IsSquareRooting2Current, CompensateInterval
    extra_keys = [
        "Wire",
        "SensorName",
        "SensorSN",
        "Id",
        "IsSquareRooting2Current",
        "CompensateInterval",
    ]

    def __init__(cls, **kwargs):
        cls._addSubclassAttributes(kwargs)

        super().__init__(**kwargs)

    def __str__(cls):
        # Use the common keys plus the extra keys (in a fixed order)
        return ",".join(str(cls.__dict__.get(k, "")) for k in [
            "Name",
            "Enabled",
            "Label",
            "ElectricalFunctionType",
            "Range",
            "Delay",
            "IsAutoRange",
            "FilteringCount",
            "SensorName",
            "SensorSN",
            "Id",
            "IsSquareRooting2Current",
            "CompensateInterval",
        ])


class DIFunctionVoltageTransmitterChannelConfig(DIFunctionChannelConfig):
    # func_type 103: Voltage Transmitter – extra: Wire, SensorName, SensorSN, Id
    extra_keys = ["Wire", "SensorName", "SensorSN", "Id"]

    def __init__(cls, **kwargs):
        cls._addSubclassAttributes(kwargs)

        super().__init__(**kwargs)


class DIFunctionCurrentTransmitterChannelConfig(DIFunctionChannelConfig):
    # func_type 104: Current Transmitter – extra: Wire, SensorName, SensorSN, Id
    extra_keys = ["Wire", "SensorName", "SensorSN", "Id"]

    def __init__(cls, **kwargs):
        cls._addSubclassAttributes(kwargs)

        super().__init__(**kwargs)


class DIFunctionStandardTCChannelConfig(DIFunctionChannelConfig):
    # func_type 105: Standard TC – extra: IsOpenDetect, SensorName, SensorSN, Id, CjcType, CJCFixedValue, CjcChannelName
    extra_keys = [
        "IsOpenDetect",
        "SensorName",
        "SensorSN",
        "Id",
        "CjcType",
        "CJCFixedValue",
        "CjcChannelName",
    ]

    def __init__(cls, **kwargs):
        cls._addSubclassAttributes(kwargs)

        super().__init__(**kwargs)


class DIFunctionCustomRTDChannelConfig(DIFunctionChannelConfig):
    # func_type 106: Custom RTD – extra: Wire, SensorName, SensorSN, Id, IsSquareRooting2Current, CompensateInterval
    extra_keys = [
        "Wire",
        "SensorName",
        "SensorSN",
        "Id",
        "IsSquareRooting2Current",
        "CompensateInterval",
    ]

    def __init__(cls, **kwargs):
        cls._addSubclassAttributes(kwargs)

        super().__init__(**kwargs)

    def __str__(cls):
        # Use the common keys plus the extra keys (in a fixed order)
        return ",".join(str(cls.__dict__.get(k, "")) for k in [
            "Name",
            "Enabled",
            "Label",
            "ElectricalFunctionType",
            "Range",
            "Delay",
            "IsAutoRange",
            "FilteringCount",
            "SensorName",
            "SensorSN",
            "Id",
            "IsSquareRooting2Current",
            "CompensateInterval",
        ])

class DIFunctionStandardResistanceChannelConfig(DIFunctionChannelConfig):
    # func_type 110: Standard Resistance – not specified in the documentation.
    extra_keys = []

    def __init__(cls, **kwargs):
        cls._addSubclassAttributes(kwargs)

        super().__init__(**kwargs)


# Mapping from ElectricalFunctionType to corresponding subclass.
def getSubclass(key):
    return {
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
    }.get(key)


# --- Channel Command Interface ---


class Channel:
    valid_names = [
        "REF1", "REF2", "CH1-01A", "CH1-01B", "CH1-02A", "CH1-02B",
        "CH1-03A", "CH1-03B", "CH1-04A", "CH1-04B", "CH1-05A", "CH1-05B",
        "CH1-06A", "CH1-06B", "CH1-07A", "CH1-07B", "CH1-08A", "CH1-08B",
        "CH1-09A", "CH1-09B", "CH1-10A", "CH1-10B"
    ]

    def __init__(cls, parent):
        cls.parent = parent

    def _validate_name(cls, name):
        if name not in cls.valid_names:
            raise ValueError(f"Invalid channel name: {name}")

    def get_configuration_json(
        cls, channel_names: List[str]
    ) -> List[DIFunctionChannelConfig]:
        for name in channel_names:
            cls._validate_name(name)
        names_str = ",".join(channel_names)
        if response := cls.parent.cmd(f'CHANnel:CONFig:JSON? "{names_str}"'):
            return coerce(response)

    def get_configuration(cls, channel_name: str) -> List[DIFunctionChannelConfig]:
        cls._validate_name(channel_name)
        if response := cls.parent.cmd(f'CHANnel:CONFig? "{channel_name}"'):
            return DIFunctionChannelConfig.from_str(response)

    def configure(cls, config: DIFunctionChannelConfig):  # Not yet implemented.
        """Set channel configuration.

        Args:
            config (DIFunctionChannelConfig): A channel configuration object.

        Returns:
            None
        """
        raise NotImplementedError("This function is not implemented yet.")
        command = f"CHANnel:CONFig {config};"
        cls.parent.send_command(command)

    def set_zero(cls, enable: bool):  # Not yet implemented.
        """Enable or disable zero clearing for a single channel.

        This command sets or cancels zero clearing for a specific channel.

        Args:
            enable (bool): True to enable zero clearing, False to cancel.

        Returns:
            None
        """
        raise NotImplementedError("This function is not implemented yet.")
        command = f"CHANnel:ZERo {int(enable)}"
        cls.parent.send_command(command)
