from datetime import datetime

class TimeTick:
    def __init__(self, TickTime: str):
        self.raw = TickTime
        self.time = datetime.strptime(TickTime, "%Y-%m-%d %H:%M:%S %f")

    def __repr__(self):
        return f"<TimeTick {self.time.isoformat()}>"

    def __eq__(self, other):
        if isinstance(other, TimeTick):
            return self.time == other.time
        if isinstance(other, datetime):
            return self.time == other
        return False

    def __lt__(self, other):
        return self.time < (other.time if isinstance(other, TimeTick) else other)

    # Add passthrough for datetime attributes if needed
    def __getattr__(self, name):
        return getattr(self.time, name)
