from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class TimeTick:
    TickTime: int
    time: datetime = None

    DOTNET_EPOCH = datetime(1, 1, 1)

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
        dt = cls.DOTNET_EPOCH + timedelta(microseconds=ticks // 10)
        return cls(dt, str(ticks))

    def to_ticks(self) -> int:
        return int((self.time - self.DOTNET_EPOCH).total_seconds() * 10_000_000)

    def to_short_format(self) -> str:
        return self.time.strftime("%Y:%m:%d %H:%M:%S %f")[:-3]

    def __getattr__(self, attr):
        return getattr(self.time, attr)
