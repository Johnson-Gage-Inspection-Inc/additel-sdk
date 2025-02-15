# unit.py - This file contains the class for the Unit commands.

# Section 1.8 - Unit commands
class Unit:
    def __init__(self, parent):
        self.parent = parent

    # 1.8.2
    def setUnitTemp(self, unit_ID, unit_name):
        """Set the temperature of the device

        Command:
            UNIT:TEMPerature <unit_ID>|<unit_name>


        Args:
            Unit: unit name or unit ID unit_name is the character string with quotation
            unit_ID: digit

        Returns:
            None
        """
        self.parent.cmd(f'UNIT:TEMPerature {unit_ID}|{unit_name}')

    # 1.8.3
    def getUnitTemp(self) -> str:
        """Query the temperature of the device

        Command:
            UNIT:TEMPerature?

        Returns:
            str: Name of temperature unit
            digit: temperature unit id
        """
        if response := self.parent.cmd("UNIT:TEMPerature?"):
            return response.split(",")
        raise ValueError("No temperature information returned.")
