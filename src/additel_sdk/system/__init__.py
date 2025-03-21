# system.py = This file contains the class for the System commands.
from datetime import date
from typing import Optional
from .communicate import Communicate
from .password import Password

# Section 1.4 - System Commands


class System:
    raise NotImplementedError("This class is not implemented yet.")
    def __init__(self, parent):
        self.parent = parent
        self.Communicate = Communicate(self)
        self.Password = Password(self)

    # 1.4.1
    def getVersion(self, module: Optional[str] = None) -> dict:
        """
        Retrieve version information for the system or a specific module.

        Command:
            SYSTem:VERSion? [<module>]

        Args:
            module (str, optional): The module for which to retrieve version information.
                Valid options include "APPLication", "ElECtricity:FIRMware", "ElECtricity:HARDware",
                "OS:FIRMware", "OS:HARDware", "JUNCtion:HARDware", "JUNCtion:FIRMware".
                If not provided, retrieves general SCIP version information.

        Returns:
            dict: A dictionary containing version information.

        Example:
            {"SCIP": "v1.0", "Application": "v1.2"}
        """
        command = f"SYSTem:VERSion? {module}" if module else "SYSTem:VERSion?"
        response = self.parent.cmd(command)
        if response:
            return {
                key_value.split(":")[0]: key_value.split(":")[1]
                for key_value in response.split(",")
            }
        return {}

    # 1.4.2
    def get_next_error(self) -> dict:
        """
        Retrieve the next error in the system error queue.

        Command:
            SYSTem:ERRor[:NEXT]?

        Returns:
            dict: A dictionary containing:
                - "error_code" (int): The error code from the system.
                - "error_message" (str): A description of the error.

        Raises:
            ValueError: If no error information is returned.
        """
        response = self.parent.cmd("SYSTem:ERRor:NEXT?")
        if response:
            parts = response.split(",")
            return {"error_code": int(parts[0]), "error_message": parts[1].strip()}
        raise ValueError("No error information returned.")

    # 1.4.3
    def set_date(self, year: int, month: int, day: int):
        """
        Set the system date.

        Command:
            SYSTem:DATE <year>,<month>,<day>

        Args:
            year (int): Year to set.
            month (int): Month to set (1-12).
            day (int): Day to set (1-31).

        Returns:
            None
        """
        command = f"SYSTem:DATE {year},{month},{day}"
        self.parent.cmd(command)

    # 1.4.4
    def get_date(self) -> date:
        """
        Query the system date.

        Command:
            SYSTem:DATE?

        Args:
            None

        Returns:
            date: The current system date.
        """
        if response := self.parent.cmd("SYSTem:DATE?"):
            return date(*map(int, response.split(",")))
        raise ValueError("No date information returned.")

    # 1.4.5
    def set_time(self, hour: int, minute: int, second: int):
        """
        Set the system time.

        Command:
            SYSTem:TIME <hour>,<minute>,<second>

        Args:
            hour (int): Hour to set (0-23).
            minute (int): Minute to set (0-59).
            second (int): Second to set (0-59).

        Returns:
            None
        """
        command = f"SYSTem:TIME {hour},{minute},{second}"
        self.parent.cmd(command)

    # 1.4.6
    def set_local_lock(self, lock: bool):
        """
        Set the local lock-out state of the system.

        Command:
            SYSTem:KLOCk <Boolean>|ON|OFF

        Args:
            lock (bool): Set to True to lock the system (ON) or False to unlock it (OFF).

        Returns:
            None
        """
        command = f"SYSTem:KLOCk {int(lock)}"
        self.parent.cmd(command)

    # 1.4.7
    def get_local_lock(self) -> bool:
        """
        Query the local lock-out state of the system.

        Command:
            SYSTem:KLOCk?

        Args:
            None

        Returns:
            bool: True if the system is locked (ON), False if unlocked (OFF).
        """
        response = self.parent.cmd("SYSTem:KLOCk?")
        if response:
            return bool(response.strip())
        raise ValueError("No lock state information returned.")

    # 1.4.8
    def set_warning_tone(self, enable: bool):
        """
        Set the state of the system's warning tone.

        Command:
            SYSTem:BEEPer:ALARm <Boolean>|ON|OFF

        Args:
            enable (bool): Set to True to enable the warning tone (ON) or False to disable it (OFF).

        Returns:
            None
        """
        command = f"SYSTem:BEEPer:ALARm {int(enable)}"
        self.parent.cmd(command)

    # 1.4.9
    def set_keypad_tone(self, enable: bool):
        """
        Set the state of the keypad tone.

        Command:
            SYSTem:BEEPer:TOUCh <Boolean>|ON|OFF

        Args:
            enable (bool): Set to True to enable the keypad tone (ON) or False to disable it (OFF).

        Returns:
            None
        """
        command = f"SYSTem:BEEPer:TOUCh {int(enable)}"
        self.parent.cmd(command)
