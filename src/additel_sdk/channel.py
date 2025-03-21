from dataclasses import dataclass
from typing import List, Optional, Type
from .coerce import coerce


@dataclass(kw_only=True)
class DIFunctionChannelConfig:
    Name: str
    Enabled: bool
    Label: str
    ElectricalFunctionType: int
    Range: int
    Delay: int
    IsAutoRange: bool
    FilteringCount: int
    IsCurrentCommutation: Optional[bool] = None
    ChannelInfo1: Optional[str] = None
    ChannelInfo2: Optional[str] = None
    ChannelInfo3: Optional[str] = None

    struct = {
        'Name': str,
        'Enabled': int,  # bool
        'Label': str,
        'ElectricalFunctionType': int,
        'Range': int,
        'Delay': int,
        'IsAutoRange': int,  # bool
        'FilteringCount': int,
    }

    def __str__(cls):
        # Use the common keys plus the extra keys (in a fixed order)
        keys_order = cls.get_keys_order()

        def serialize(value):
            if isinstance(value, bool):
                return "1" if value else "0"
            return str(value) if value is not None else ""

        return ",".join(serialize(getattr(cls, k, "")) for k in keys_order)

    @classmethod
    def from_str(cls, data: str):
        if ";" in data:
            parts = [p for p in data.split(";") if p]
            return [cls.from_str(p) for p in parts]
        values = data.split(",")
        func_type = int(values[3])
        if subclass := getSubclass(func_type):
            return subclass._from_str(data)
        raise ValueError(f"Unsupported ElectricalFunctionType: {func_type}")

    @classmethod
    def _from_str(cls, data: str):
        values = data.split(",")
        keys_order = cls.get_keys_order()
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

    @classmethod
    def expected_types(cls):
        common_types = [str, bool, str, int, int, int, bool, int]
        return common_types + cls.extra_types()

    @classmethod
    def extra_types(cls):
        return []


@dataclass
class DIFunctionVoltageChannelConfig(DIFunctionChannelConfig):
    """Voltage Function Channel Configuration"""
    highImpedance: Optional[int] = None

    @classmethod
    def extra_types(cls):
        return [int]

    extra_keys = ["highImpedance"]


@dataclass
class DIFunctionCurrentChannelConfig(DIFunctionChannelConfig):
    @classmethod
    def extra_types(cls):
        return []

    extra_keys = []


@dataclass
class DIFunctionResistanceChannelConfig(DIFunctionChannelConfig):
    """func_type 2: Resistance – extra parameters: Wire (int), IsOpenDetect (int)"""
    Wire: int
    IsOpenDetect: int

    @classmethod
    def extra_types(cls):
        return [int, int]

    extra_keys = ["Wire", "IsOpenDetect"]


@dataclass
class DIFunctionRTDChannelConfig(DIFunctionChannelConfig):
    """func_type 3: RTD – extra parameters: Wire, SensorName, SensorSN, Id, IsSquareRooting2Current, CompensateInterval"""
    Wire: int
    SensorName: str
    SensorSN: Optional[str]
    Id: Optional[str]
    IsSquareRooting2Current: int
    CompensateInterval: int

    @classmethod
    def extra_types(cls):
        return [int, str, str, str, int, int]

    extra_keys = [
        "Wire",
        "SensorName",
        "SensorSN",
        "Id",
        "IsSquareRooting2Current",
        "CompensateInterval",
    ]

    @classmethod
    def _from_str(cls, data: str):
        struct = {
            **DIFunctionChannelConfig.struct,
            "Wire": int,
            "SensorName": str,
            "SensorSN": str,
            "Id": str,
            "IsSquareRooting2Current": int,
            "CompensateInterval": int
        }
        # kwargs = {}
        # for k, v, t in zip(struct.keys(), data.split(","), struct.values()):
        #     kwargs[k] =
        # return cls(**kwargs)
        return cls(**{k: t(v) if v != "" else None for k, v, t in zip(struct.keys(), data.split(","), struct.values())})


@dataclass
class DIFunctionThermistorChannelConfig(DIFunctionChannelConfig):
    """func_type 4: Thermistor – extra parameters: Wire, SensorName, SensorSN, Id"""

    Wire: int
    SensorName: str
    SensorSN: Optional[str]
    Id: Optional[str]

    @classmethod
    def extra_types(cls):
        return [int, str, str, str]

    extra_keys = ["Wire", "SensorName", "SensorSN", "Id"]


@dataclass
class DIFunctionTCChannelConfig(DIFunctionChannelConfig):
    """func_type 100: Thermocouple (TC) – extra: IsOpenDetect, SensorName, SensorSN, Id, CjcType, CJCFixedValue, CjcChannelName"""
    IsOpenDetect: int
    SensorName: str
    SensorSN: Optional[str]
    Id: Optional[str]
    CjcType: Optional[int]
    CJCFixedValue: Optional[float]
    CjcChannelName: Optional[str]

    @classmethod
    def extra_types(cls):
        return [int, str, str, str, int, float, str]

    extra_keys = [
        "IsOpenDetect",
        "SensorName",
        "SensorSN",
        "Id",
        "CjcType",
        "CJCFixedValue",
        "CjcChannelName",
    ]


@dataclass
class DIFunctionSwitchChannelConfig(DIFunctionChannelConfig):
    """func_type 101: Switch – not specified in the documentation."""
    @classmethod
    def extra_types(cls):
        return []

    extra_keys = []


@dataclass
class DIFunctionSPRTChannelConfig(DIFunctionChannelConfig):
    """func_type 102: SPRT – extra: Wire, SensorName, SensorSN, Id, IsSquareRooting2Current, CompensateInterval"""
    Wire: int
    SensorName: str
    SensorSN: str
    Id: str
    IsSquareRooting2Current: int
    CompensateInterval: int

    @classmethod
    def extra_types(cls):
        return [int, str, str, str, int, int]

    extra_keys = [
        "Wire",
        "SensorName",
        "SensorSN",
        "Id",
        "IsSquareRooting2Current",
        "CompensateInterval",
    ]


@dataclass
class DIFunctionVoltageTransmitterChannelConfig(DIFunctionChannelConfig):
    """func_type 103: Voltage Transmitter – extra: Wire, SensorName, SensorSN, Id"""
    Wire: int
    SensorName: str
    SensorSN: Optional[str]
    Id: Optional[str]

    @classmethod
    def extra_types(cls):
        return [int, str, str, str]

    extra_keys = ["Wire", "SensorName", "SensorSN", "Id"]


@dataclass
class DIFunctionCurrentTransmitterChannelConfig(DIFunctionChannelConfig):
    """func_type 104: Current Transmitter – extra: Wire, SensorName, SensorSN, Id"""
    Wire: int
    SensorName: str
    SensorSN: Optional[str]
    Id: Optional[str]

    @classmethod
    def extra_types(cls):
        return [int, str, str, str]

    extra_keys = ["Wire", "SensorName", "SensorSN", "Id"]


@dataclass
class DIFunctionStandardTCChannelConfig(DIFunctionChannelConfig):
    """func_type 105: Standard TC – extra: IsOpenDetect, SensorName, SensorSN, Id, CjcType, CJCFixedValue, CjcChannelName"""
    IsOpenDetect: int
    SensorName: str
    SensorSN: Optional[str]
    Id: Optional[str]
    CjcType: Optional[int]
    CJCFixedValue: Optional[float]
    CjcChannelName: Optional[str]

    @classmethod
    def extra_types(cls):
        return [int, str, str, str, int, float, str]

    extra_keys = [
        "IsOpenDetect",
        "SensorName",
        "SensorSN",
        "Id",
        "CjcType",
        "CJCFixedValue",
        "CjcChannelName",
    ]


@dataclass
class DIFunctionCustomRTDChannelConfig(DIFunctionChannelConfig):
    """func_type 106: Custom RTD – extra: Wire, SensorName, SensorSN, Id, IsSquareRooting2Current, CompensateInterval"""
    Wire: int
    SensorName: str
    SensorSN: str
    Id: str
    IsSquareRooting2Current: int
    CompensateInterval: int

    @classmethod
    def extra_types(cls):
        return [int, str, str, str, int, int]

    extra_keys = [
        "Wire",
        "SensorName",
        "SensorSN",
        "Id",
        "IsSquareRooting2Current",
        "CompensateInterval",
    ]


@dataclass
class DIFunctionStandardResistanceChannelConfig(DIFunctionChannelConfig):
    @classmethod
    def extra_types(cls):
        return []

    extra_keys = []


def getSubclass(key: int) -> Type[DIFunctionChannelConfig]:
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
    }[key]


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

    def get_configuration_json(cls, channel_names: List[str]) -> List[DIFunctionChannelConfig]:
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
