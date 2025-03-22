import os
import csv
from typing import List, Union
import src.additel_sdk.appendices as appendices 

# Section 1.8 - Unit commands
class Unit:
    unit_lookup = {}
    with open(os.path.join(appendices.__path__[0], 'unit_lookup.csv'),
                mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Adjust the keys below to match your CSV headers
            unit_id = row['Unit_Id'].strip()
            unit_value = row['Unit'].strip()
            unit_lookup[unit_id] = unit_value

    def __init__(self, parent):
        self.parent = parent

    # 1.8.2
    def setUnitTemp(self, unit: Union[int, str]) -> None:
        """Set the temperature unit of the device

        Command:
            UNIT:TEMPerature <unit_ID>|<unit_name>

        Args:
            unit: digit (unit identifier) OR unit name as a string (should be quoted if needed)
        """
        if isinstance(unit, int):
            # If unit is an integer, use it directly
            unit_str = str(unit)
            if unit_str not in self.unit_lookup:
                raise ValueError(f"Unit ID '{unit_str}' not found in lookup table.")
            unit = unit_str
        elif isinstance(unit, str):
            # If unit is a string, find the corresponding ID
            found_id = next((uid for uid, name in self.unit_lookup.items() if name.lower() == unit.lower()), None)
            if found_id is None:
                raise ValueError(f"Unit name '{unit}' not found in lookup table.")
            unit = found_id
        else:
            raise TypeError("Unit must be either a string (unit name) or an integer (unit ID).")
        self.parent.send_command(f"UNIT:TEMPerature {unit}")

    # 1.8.3
    def get_unit_temp(self) -> List[str]:
        """Query the temperature unit of the device

        Command:
            UNIT:TEMPerature?

        Returns:
            A list containing the unit name and the temperature unit id.
        """
        if response := self.parent.cmd("UNIT:TEMPerature?"):
            return response.split(",")
        raise ValueError("No temperature information returned.")
