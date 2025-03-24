from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Union


@dataclass
class TimeTick:
    TickTime: Union[str, int]
    time: datetime = field(init=False)

    def __post_init__(self):
        if isinstance(self.TickTime, int) or (isinstance(self.TickTime, str) and self.TickTime.isdigit()):
            ticks = int(self.TickTime)
            self.time = datetime(1, 1, 1) + timedelta(microseconds=ticks // 10)
        elif isinstance(self.TickTime, str):
            try:
                self.time = datetime.strptime(self.TickTime, "%Y-%m-%d %H:%M:%S %f")
            except ValueError:
                try:
                    self.time = datetime.strptime(self.TickTime, "%Y:%m:%d %H:%M:%S %f")
                except ValueError as e:
                    raise ValueError("Unrecognized datetime format") from e
        else:
            raise TypeError("Input must be an int or str")

    def to_ticks(self) -> int:
        "long timestamp format (ticks since 1/1/0001)"
        return int((self.time - datetime(1, 1, 1)).total_seconds() * 1e7)

    def to_short_format(self) -> str:
        return self.time.strftime("%Y:%m:%d %H:%M:%S %f")[:-3]

    def __getattr__(self, attr):
        return getattr(self.time, attr)