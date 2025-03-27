# system.py = This file contains the class for the System commands.
from datetime import date
from typing import Optional, TYPE_CHECKING
from .communicate import Communicate
from .password import Password
import logging

if TYPE_CHECKING:
    from src.additel_sdk import Additel

# Section 1.4 - System Commands


class System:
    def __init__(self, parent: "Additel"):
        self.parent = parent
        self.Communicate = Communicate(self)
        self.Password = Password(self)

    # 1.4.1
    def get_version(self) -> str:
        """Retrieve version information for the system or a specific module.

        Command:
            SYSTem:VERSion?

        Returns:
            dict: A dictionary containing version information.

        Example:
            {"SCIP": "v1.0", "Application": "v1.2"}
        """
        return self.parent.cmd("SYSTem:VERSion?")

    # 1.4.2
    def get_error(self, next=False) -> dict:
        """Retrieve the next error in the system error queue.

        Command:
            SYSTem:ERRor[:NEXT]?

        Returns:
            dict: A dictionary containing:
                - "error_code" (int): The error code from the system.
                - "error_message" (str): A description of the error.

        Raises:
            ValueError: If no error information is returned.
        """
        command = f"SYSTem:ERRor{':NEXT' if next else ''}?"
        if response := self.parent.cmd(command):
            parts = response.split(",")
            return {"error_code": int(parts[0]), "error_message": parts[1].strip()}
        raise ValueError("No error information returned.")

    # 1.4.3
    def set_date(self, year: int, month: int, day: int) -> None:
        """Set the system date.

        Command:
            SYSTem:DATE <year>,<month>,<day>

        Args:
            year (int): Year to set.
            month (int): Month to set (1-12).
            day (int): Day to set (1-31).
        """
        command = f"SYSTem:DATE {year},{month},{day}"
        self.parent.send_command(command)

    # 1.4.4
    def get_date(self) -> date:
        """Query the system date.

        Command:
            SYSTem:DATE?

        Returns:
            date: The current system date.
        """
        if response := self.parent.cmd("SYSTem:DATE?"):
            return date(*map(int, response.split(",")))
        raise ValueError("No date information returned.")

    # 1.4.5
    def set_time(self, hour: int, minute: int, second: int) -> None:
        """Set the system time.

        Command:
            SYSTem:TIME <hour>,<minute>,<second>

        Args:
            hour (int): Hour to set (0-23).
            minute (int): Minute to set (0-59).
            second (int): Second to set (0-59).
        """
        command = f"SYSTem:TIME {hour},{minute},{second}"
        self.parent.send_command(command)

    # 1.4.6
    def set_local_lock(self, lock: bool) -> None:
        """Set the local lock-out state of the system.

        Command:
            SYSTem:KLOCk <Boolean>|ON|OFF

        Args:
            lock (bool): Set to True to lock the system (ON) or False to unlock it (OFF).
        """
        command = f"SYSTem:KLOCk {int(lock)}"
        self.parent.send_command(command)

    # 1.4.7
    def get_local_lock(self) -> bool:
        """Query the local lock-out state of the system.

        Command:
            SYSTem:KLOCk?
        Returns:
            bool: True if the system is locked (ON), False if unlocked (OFF).
        """
        response = self.parent.cmd("SYSTem:KLOCk?")
        if response:
            return bool(response.strip())
        raise ValueError("No lock state information returned.")

    # 1.4.8
    def set_warning_tone(self, enable: bool) -> None:
        """Set the state of the system's warning tone.

        Command:
            SYSTem:BEEPer:ALARm <Boolean>|ON|OFF

        Args:
            enable (bool): Set to True to enable the warning tone (ON) or False to disable it (OFF).
        """
        command = f"SYSTem:BEEPer:ALARm {int(enable)}"
        self.parent.send_command(command)

    # 1.4.9
    def set_keypad_tone(self, enable: bool) -> None:
        """Set the state of the keypad tone.

        Command:
            SYSTem:BEEPer:TOUCh <Boolean>|ON|OFF

        Args:
            enable (bool): Set to True to enable the keypad tone (ON) or False to disable it (OFF).
        """
        command = f"SYSTem:BEEPer:TOUCh {int(enable)}"
        self.parent.send_command(command)

    def flush_error_queue(system):
        i = 0
        while True:
            err = system.get_error(next=True)
            print(err)
            if err['error_code'] == 0:
                break
            i += 1
        logging.debug(f"Flushed {i} errors.")
