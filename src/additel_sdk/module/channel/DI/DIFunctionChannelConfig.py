from dataclasses import dataclass, field, fields, MISSING
from typing import Optional, Type, Union, get_origin, get_args


@dataclass(kw_only=True)
class DIFunctionChannelConfig:
    """Base class for function channel configuration.

    Attributes:
        Name (str): The name of the channel.
        Enabled (bool): Whether the channel is enabled.
        Label (str): The label of the channel.
        ElectricalFunctionType (int): The type of electrical function.
        Range (int): The range of the channel.
        Delay (int): The delay for the channel.
        IsAutoRange (bool): Whether auto-ranging is enabled.
        FilteringCount (int): The filtering count.
        IsCurrentCommutation (Optional[bool]): Whether current commutation is enabled.
    """
    Name: str
    Enabled: bool = field(metadata={"cast": int})
    Label: str
    ElectricalFunctionType: int
    Range: int
    Delay: int
    IsAutoRange: bool = field(metadata={"cast": int})
    FilteringCount: int
    IsCurrentCommutation: Optional[bool] = field(default=None, metadata={"cast": int})
    ChannelInfo1: Optional[str] = None
    ChannelInfo2: Optional[str] = None
    ChannelInfo3: Optional[str] = None

    def __str__(self: Type["DIFunctionChannelConfig"]) -> str:
        """Serialize the channel configuration to a string.

        Args:
            self (Type[&quot;DIFunctionChannelConfig&quot;]): The channel configuration
            object.

        Returns:
            str: The serialized channel configuration.
        """

        def serialize(value):
            if value is None:
                return ""
            if isinstance(value, bool):
                return "1" if value else "0"
            return str(value)

        required_fields = [
            f
            for f in fields(self)
            if f.default is MISSING and f.default_factory is MISSING
        ]
        return ",".join(serialize(getattr(self, f.name)) for f in required_fields)

    @classmethod
    def from_str(cls, data: str) -> "DIFunctionChannelConfig":
        """Deserialize the channel configuration from a string.

        Args:
            data (str): The serialized channel configuration.

        Raises:
            ValueError: If the ElectricalFunctionType is not supported.

        Returns:
            DIFunctionChannelConfig: The deserialized channel configuration.
        """
        if ";" in data:
            return [cls.from_str(p) for p in data.split(";") if p]
        values = data.split(",")
        func_type = int(values[3])
        if subclass := getSubclass(func_type):
            required_fields = [
                f
                for f in fields(subclass)
                if f.default is MISSING and f.default_factory is MISSING
            ]

            def _cast_value(v: str, f: field):
                if v == "":
                    return None
                caster = _resolve_caster(f)
                if caster is bool:
                    return bool(int(v))
                return caster(v)

            def _resolve_caster(f: field) -> Type:
                annotation = f.metadata.get("cast", f.type)
                if get_origin(annotation) is Union:
                    args = [
                        arg for arg in get_args(annotation) if arg is not type(None)
                    ]
                    return args[0] if args else str
                return annotation

            parsed = {
                f.name: _cast_value(v, f) for f, v in zip(required_fields, values)
            }

            return subclass(**parsed)
        raise ValueError(f"Unsupported ElectricalFunctionType: {func_type}")


@dataclass
class DIFunctionVoltageChannelConfig(DIFunctionChannelConfig):
    """func_type 0: Voltage – Function Channel Configuration"""

    highImpedance: int = None


@dataclass
class DIFunctionCurrentChannelConfig(DIFunctionChannelConfig):
    """func_type 1: Current – extra parameters: None"""

    pass


@dataclass
class DIFunctionResistanceChannelConfig(DIFunctionChannelConfig):
    """func_type 2: Resistance
    
    extra parameters:
        wires,
        positive and negative current
    """

    Wire: int
    IsOpenDetect: bool = field(metadata={"cast": int})


@dataclass
class DIFunctionRTDChannelConfig(DIFunctionChannelConfig):
    """func_type 3: RTD – 
    
    extra parameters:
        Sensor Name,
        wires,
        compensation interval,
        whether 1.4 times current
    """

    Wire: int
    SensorName: str
    SensorSN: str
    Id: str
    IsSquareRooting2Current: bool = field(metadata={"cast": int})
    CompensateInterval: int


@dataclass
class DIFunctionThermistorChannelConfig(DIFunctionChannelConfig):
    """func_type 4: Thermistor – extra parameters: Sensor Name, wires"""

    Wire: int
    SensorName: str


@dataclass
class DIFunctionTCChannelConfig(DIFunctionChannelConfig):
    """func_type 100: Thermocouple (TC) – extra:
    sensor name, whether the break couple
    detection, cold junction type, cold
    junction fixed value, custom cold
    junction channel name
    """

    IsOpenDetect: bool = field(metadata={"cast": int})
    SensorName: str
    CjcType: int
    CJCFixedValue: float
    CjcChannelName: str


@dataclass
class DIFunctionSwitchChannelConfig(DIFunctionChannelConfig):
    """func_type 101: Switch – extra: switch type"""

    SwitchType: int  # NOTE: The key might not be exactly right


@dataclass
class DIFunctionSPRTChannelConfig(DIFunctionChannelConfig):
    """func_type 102: SPRT

    Attributes:
        Wire (int): wires
        SensorName (str): Sensor Name
        SensorSN (str): Sensor Serial Number
        Id (str): Sensor ID
        IsSquareRooting2Current (bool): Whether to open 1.4 times current
        CompensateInterval (int): Compensation interval
    """

    Wire: int
    SensorName: str
    SensorSN: str
    Id: str
    IsSquareRooting2Current: bool = field(metadata={"cast": int})
    CompensateInterval: int


@dataclass
class DIFunctionVoltageTransmitterChannelConfig(DIFunctionChannelConfig):
    """func_type 103: Voltage Transmitter – extra: Wire, SensorName, SensorSN, Id"""

    Wire: int
    SensorName: str
    SensorSN: str
    Id: str


@dataclass
class DIFunctionCurrentTransmitterChannelConfig(DIFunctionChannelConfig):
    """func_type 104: Current Transmitter – extra: Wire, SensorName, SensorSN, Id"""

    Wire: int
    SensorName: str
    SensorSN: str
    Id: str


@dataclass
class DIFunctionStandardTCChannelConfig(DIFunctionChannelConfig):
    """func_type 105: Standard TC – extra: IsOpenDetect, SensorName, SensorSN, Id, CjcType, CJCFixedValue, CjcChannelName"""

    IsOpenDetect: bool = field(metadata={"cast": int})
    SensorName: str
    SensorSN: str
    Id: str
    CjcType: int
    CJCFixedValue: float
    CjcChannelName: str


@dataclass
class DIFunctionCustomRTDChannelConfig(DIFunctionChannelConfig):
    """func_type 106: Custom RTD – extra: Sensor Name, wires, compensation interval, whether 1.4 times current"""

    Wire: int
    SensorName: str
    SensorSN: str
    Id: str
    IsSquareRooting2Current: bool = field(metadata={"cast": int})
    CompensateInterval: int


@dataclass
class DIFunctionStandardResistanceChannelConfig(DIFunctionChannelConfig):
    """func_type 110: Standard Resistance – extra: None?"""

    pass


def getSubclass(key: int) -> Type[DIFunctionChannelConfig]:
    return {
        0:   DIFunctionVoltageChannelConfig,
        1:   DIFunctionCurrentChannelConfig,
        2:   DIFunctionResistanceChannelConfig,
        3:   DIFunctionRTDChannelConfig,
        4:   DIFunctionThermistorChannelConfig,
        100: DIFunctionTCChannelConfig,
        101: DIFunctionSwitchChannelConfig,
        102: DIFunctionSPRTChannelConfig,
        103: DIFunctionVoltageTransmitterChannelConfig,
        104: DIFunctionCurrentTransmitterChannelConfig,
        105: DIFunctionStandardTCChannelConfig,
        106: DIFunctionCustomRTDChannelConfig,
        110: DIFunctionStandardResistanceChannelConfig,
    }[key]
