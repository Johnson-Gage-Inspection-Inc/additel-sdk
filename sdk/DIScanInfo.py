# DIScanInfo.py
class DIScanInfo:
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
    def from_json(cls, data: dict):
        """Create a DIScanInfo object from a JSON object.

        Parameters:
            data (dict): A dictionary containing the scan information.

        Returns:
            DIScanInfo: An instance of DIScanInfo populated with the JSON data.
        """
        return cls(
            NPLC=data.get("NPLC"),
            ChannelName=data.get("ChannelName")
        )

    @classmethod
    def from_str(cls, data: str):
        """Parse the scanning information from a string.

        Parameters:
            data (str): A comma-separated string containing the scan information.

        Returns:
            DIScanInfo: An instance of DIScanInfo populated with the string data.
        """
        values = data.split(',')
        NPLC = int(values[0])
        ChannelName = str(values[1])
        return cls(NPLC=NPLC, ChannelName=ChannelName)

    def to_json(self):
        """Convert the DIScanInfo object to a JSON-compatible dictionary."""
        return {
            "NPLC": self.NPLC,
            "ChannelName": self.ChannelName
        }

    def to_str(self):
        """Convert the DIScanInfo object to a string representation."""
        return f"{self.NPLC},{self.ChannelName}"

    def __str__(self):
        """Override the built-in str() function."""
        return self.to_str()

    def __dict__(self):
        """Override the built-in dict() function."""
        return self.to_json()

    def __repr__(self):
        """Override the built-in repr() function with the one from the dict class"""
        return self.to_json().__repr__()
