from dataclasses import dataclass, field
from datetime import datetime as dt, timedelta as tΔ


@dataclass
class TimeTick:
    TickTime: str
    time: dt = field(init=False)

    def __post_init__(self):
        if '-' in self.TickTime:
            self.time = dt.strptime(self.TickTime, "%Y-%m-%d %H:%M:%S %f")
        elif ':' in self.TickTime:
            self.time = dt.strptime(self.TickTime, "%Y:%m:%d %H:%M:%S %f")
        else:
            self.time = dt(1, 1, 1) + tΔ(seconds=int(self.TickTime) / 1e7)

    def to_ticks(self) -> int:
        "long timestamp format (ticks since 1/1/0001)"
        return int((self.time - dt(1, 1, 1)).total_seconds() * 1e7)

    def to_short_format(self) -> str:
        return self.time.strftime("%Y:%m:%d %H:%M:%S %f")[:-3]

    def __getattr__(self, attr):
        return getattr(self.time, attr)
