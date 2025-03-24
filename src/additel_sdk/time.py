from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class TimeTick:
    TickTime: str
    time: datetime = field(init=False)

    def __post_init__(self):
        self.time = datetime.strptime(self.TickTime, "%Y-%m-%d %H:%M:%S %f")

    @classmethod
    def from_iso_string(cls, s: str) -> "TimeTick":
        return cls(datetime.strptime(s, "%Y-%m-%d %H:%M:%S %f"), s)

    @classmethod
    def from_short_format(cls, s: str) -> "TimeTick":
        return cls(datetime.strptime(s, "%Y:%m:%d %H:%M:%S %f"), s)

    @classmethod
    def from_ticks(cls, ticks: int) -> "TimeTick":
        dt = datetime(1, 1, 1) + timedelta(microseconds=int(ticks) // 10)
        return cls(dt.strftime("%Y-%m-%d %H:%M:%S %f"))

    def to_ticks(self) -> int:
        return int((self.time - datetime(1, 1, 1)).total_seconds() * 1e7)

    @classmethod
    def to_short_format(self) -> str:
        return self.time.strftime("%Y:%m:%d %H:%M:%S %f")[:-3]

    def __getattr__(self, attr):
        return getattr(self.time, attr)
