# DIScanInfo.py
class DIScanInfo(dict):
    """Data structure for scanning information.

    Each configuration includes:
        NPLC (int): Number of Power Line Cycles (NPLC).
        ChannelName (int): Sampling frequency cycle.
        ClassName
    """
    def __init__(self,
                NPLC: int,
                ChannelName: str):
        self.NPLC = NPLC  # Number of Power Line Cycles (NPLC)
        self.ChannelName = ChannelName  # Sampling frequency cycle

    @classmethod
    def from_str(cls, data: str):
        """Parse the scanning information from a string.

        Args:
            data (str): A comma-separated string containing the scan information.

        Returns:
            DIScanInfo: An instance of DIScanInfo populated with the string data.
        """
        values = data.split(',')
        NPLC = int(values[0])
        ChannelName = str(values[1])
        return cls(NPLC=NPLC, ChannelName=ChannelName)

    def __dict__(self):
        """Convert the DIScanInfo object to a JSON-compatible dictionary."""
        return {
            "NPLC": self.NPLC,
            "ChannelName": self.ChannelName
        }

    def __str__(self):
        """Convert the DIScanInfo object to a string representation."""
        return f"{self.NPLC},{self.ChannelName}"
