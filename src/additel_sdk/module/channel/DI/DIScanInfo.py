from dataclasses import dataclass


@dataclass
class DIScanInfo:
    NPLC: int
    ChannelName: str

    @classmethod
    def from_str(cls, data: str) -> "DIScanInfo":
        """Parse the scanning information from a string."""
        NPLC, ChannelName = data.split(",")
        return cls(NPLC=int(NPLC), ChannelName=ChannelName)

    def __str__(self) -> str:
        """Convert the DIScanInfo object to a string representation."""
        return f"{self.NPLC},{self.ChannelName}"
