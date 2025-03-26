from datetime import datetime as dt, timedelta as tΔ


class TimeTick(dt):
    def __new__(cls, TickTime):
        if '-' in TickTime:
            t = dt.strptime(TickTime, "%Y-%m-%d %H:%M:%S %f")
        elif ':' in TickTime:
            t = dt.strptime(TickTime, "%Y:%m:%d %H:%M:%S %f")
        else:
            t = dt(1, 1, 1) + tΔ(seconds=int(TickTime) / 1e7)
        return dt.__new__(
            cls,
            t.year,
            t.month,
            t.day,
            t.hour,
            t.minute,
            t.second,
            t.microsecond,
        )

    def to_ticks(self) -> int:
        "long timestamp format (ticks since 1/1/0001)"
        return round((self - dt(1, 1, 1)).total_seconds() * 1e7)

    def to_short_format(self) -> str:
        return self.strftime("%Y:%m:%d %H:%M:%S %f")[:-3]
