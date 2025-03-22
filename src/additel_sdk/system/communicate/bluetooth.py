# system\communicate\bluetooth.py


class Bluetooth:
    def __init__(self, parent):
        self.parent = parent

    # 1.4.43
    def setstate(self, enable: bool) -> None:
        """Set the state of the system's Bluetooth functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:BLUetooth[:STATe] <Boolean>|ON|OFF

        Args:
            enable (bool): Set to True to enable Bluetooth (ON) or False to disable it (OFF).
        """
        command = f"SYSTem:COMMunicate:SOCKet:BLUetooth:STATe {int(enable)}"
        self.parent.cmd(command)

    # 1.4.44
    def getstate(self) -> bool:
        """Query the state of the system's Bluetooth functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:BLUetooth[:STATe]?
        Returns:
            bool: True if Bluetooth is enabled (ON), False if disabled (OFF).
        """
        response = self.parent.cmd("SYSTem:COMMunicate:SOCKet:BLUetooth:STATe?")
        if response:
            return bool(response.strip())
        raise ValueError("No Bluetooth state information returned.")

    # 1.4.45
    def getName(self) -> str:
        """Query the name of the Bluetooth device.

        Command:
            SYSTem:COMMunicate:BLUEtooth:NAMe?

        Returns:
            str: The name of the Bluetooth device.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:BLUEtooth:NAMe?"):
            return response.strip()
        raise ValueError("No Bluetooth name information returned.")

    # 1.4.46 (SYSTem:COMMunicate:BLUEtooth:NAMe<UnquoStr>))
    def setName(self, name: str) -> None:
        """Set the name of the Bluetooth device.

        Command:
            SYSTem:COMMunicate:BLUEtooth:NAMe <UnquoStr>

        Args:
            name (str): The name to set.
        """
        self.parent.cmd(f"SYSTem:COMMunicate:BLUEtooth:NAMe {name}")
