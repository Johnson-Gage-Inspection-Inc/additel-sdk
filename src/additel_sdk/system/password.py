# system\password.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.additel_sdk.system import System


class Password:
    def __init__(self, parent: "System"):
        self.parent = parent

    # 1.4.40
    def setPassword(
        self, old_password: str, new_password: str, new_password_confirm: str
    ) -> None:
        """Edit the user password

        Command:
            SYSTem:PASSword <password>

        Args:
            old_password (str): The old password.
            new_password (str): The new password.
            new_password_confirm (str): The new password confirmation.
        """
        self.parent.parent.send_command(
            f"SYSTem:PASSword {old_password},{new_password},{new_password_confirm}"
        )

    # 1.4.41
    def getProtection(self) -> bool:
        """Query that the protection of sensor bank
        password is opened or not

        Command:
            SYSTem:PASSword:ENABle:SENSor?
        Returns:
            bool: True if the protection of sensor bank password is opened, False if not.
        """
        if response := self.parent.parent.cmd("SYSTem:PASSword:ENABle:SENSor?"):
            return bool(response.strip())
        raise ValueError("No protection information returned.")

    # 1.4.42
    def setProtection(self, enable: bool) -> None:
        """Set the protection of sensor bank password

        Command:
            SYSTem:PASSword:ENABle:SENSor <enable>

        Args:
            enable (bool): Set to True to enable the protection of sensor bank password.
        """
        self.parent.parent.send_command(f"SYSTem:PASSword:ENABle:SENSor {int(enable)}")
