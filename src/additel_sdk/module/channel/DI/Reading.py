
from .TimeTick import TimeTick
from dataclasses import dataclass, field, fields
from typing import Optional, List, get_origin, get_args

def count_decimals(value: float) -> int:
    """Return the number of decimals for a float value."""
    s = str(value)
    return len(s.split(".")[1]) if "." in s else 0

@dataclass
class DIReading:
    ChannelName: str
    Unit: int
    ValuesCount: int = 0
    DateTimeTicks: List[TimeTick] = field(default_factory=list)
    Values: List[float] = field(default_factory=list)
    ValuesFiltered: List[float] = field(default_factory=list)
    ValueDecimals: Optional[int] = None

    def __post_init__(self):
        self._post_init_common()

    def _post_init_common(self):
        from .. import Channel
        self.ValuesCount = len(self.Values)
        if self.ValueDecimals is None:
            self.ValueDecimals = count_decimals(self.Values[0])
        Channel.validate_name(self.ChannelName)


@dataclass
class DIElectricalReading(DIReading):
    pass


@dataclass
class DITCReading(DIReading):
    NumElectrical: int = 0
    CJCs: List[int] = field(default_factory=list)
    CJCUnit: int = 0
    CjcRaws: List[float] = field(default_factory=list)
    CJCRawsUnit: int = 0
    CJCDecimals: int = 0
    TempValues: List[float] = field(default_factory=list)
    TempUnit: int = 0
    TempDecimals: int = 0


@dataclass
class DITemperatureReading(DIReading):
    """

    Args:
        DIReading (_type_): _description_

    Attributes:
        TempValues (list[float]): List of temperature values.
        TempUnit (int): Temperature unit identifier.
        TempDecimals (int): Number of decimal places for temperature values.
        ValueDecimals (int): the number of decimals from the raw value string

    Returns:
        _type_: _description_
    """
    TempUnit: int = 0
    TempValuesCount: int = 0
    TempValues: list[float] = field(default_factory=list)
    TempDecimals: Optional[int] = 4  # e.g. usually 4

    def __post_init__(self):
        super()._post_init_common()
        self.TempValuesCount = len(self.TempValues)
        if self.TempDecimals is None and self.TempValues:
            self.TempDecimals = count_decimals(self.TempValues[0])

    @classmethod
    def from_str(cls, input: str) -> "DITemperatureReading":
        treated_input = input[1:-2].replace("------", '-inf')
        array = [reading.split(",") for reading in treated_input.split(";")]
        transposed = list(map(list, zip(*array)))
        fs = [f for f in fields(cls)[:-1] if f.name != "ValueDecimals"]
        values = {}
        for i, f in enumerate(fs):
            if get_origin(f.type) is list:
                (type_,) = get_args(f.type)
                values[f.name] = [type_(v) for v in transposed[i]]
            else:
                first_value = f.type(transposed[i][0])
                if values.get(f.name) is None:
                    values[f.name] = first_value if transposed[i] else None
                else:
                    assert values[f.name] == first_value, "Unexpected type"
        return cls(**values)

    def __str__(self):
        def fmt(val, dec):
            return f"{round(val, dec):.{dec}f}"

        parts = []
        for i in range(len(self.Values)):
            ticks = self.DateTimeTicks[i].to_ticks()
            parts.append(
                f"{self.ChannelName},{self.Unit},1,{ticks},"
                f"{fmt(self.Values[i], self.ValueDecimals)},"
                f"{fmt(self.ValuesFiltered[i], self.ValueDecimals)},"
                f"{self.TempUnit},1,"
                f"{fmt(self.TempValues[i], self.TempDecimals)};"
            )
        return '"' + "".join(parts) + '"'

