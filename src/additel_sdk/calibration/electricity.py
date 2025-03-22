from typing import List


class Electricity:

    def __init__(self, parent):
        self.parent = parent

    def start_scan(self, function: int, range_: int, mode: int = 0) -> None:
        """
        Start an electrical calibration scan.

        This method initiates a calibration scan for electrical parameters
        based on the specified mode, function, and range.

        Args:
            function (int): The function type for calibration:
                - 0: Voltage
                - 1: Current
                - 2: Resistance
                - 3: PRT (Platinum Resistance Thermometer)
                - 4: Thermistor
            range_ (int): The range of calibration specific to the function type:
                - Voltage: 0 (100 mV), 1 (1 V), 2 (10 V), 3 (50 V)
                - Current: 0 (100 µA), 1 (1 mA), 2 (10 mA), 3 (100 mA)
                - Resistance: 0 (100 Ω), 1 (1 kΩ), 2 (10 kΩ), 3 (100 kΩ),
                4 (1 MΩ), 5 (10 MΩ), 6 (100 MΩ)
                - PRT: 0 (100 Ω), 1 (400 Ω), 2 (4 kΩ)
                - Thermistor: 0 (0–10 kΩ), 1 (10–100 kΩ), 2 (0.1–1 MΩ)
            mode (int): The mode of calibration. Only `0` (active calibration) is supported. Defaults to 0.

        Raises:
            ValueError: If `mode` is not 0, or if invalid parameters are provided.
        """
        if mode != 0:
            raise ValueError("Only mode 0 (active calibration) is supported")
        command = f"CALibration:ElECtricity:SCAN {mode},{function},{range_}"
        self.parent.send_command(command)

    def get_scan_data(self) -> dict:
        """
        Retrieve the original data of electrical logging during calibration.

        Command:
            CALibration:ElECtricity:SCAN?

        Args:
            None

        Returns:
            dict: A dictionary containing the following keys:
                - 'exception_code': 4-byte exception code.
                - 'mode': Mode of calibration (e.g., active calibration).
                - 'function': Function type (voltage, current, resistance, etc.).
                - 'range': Calibration range.
                - 'status': Indicates if data is available (1 for available, 0 otherwise).
                - 'data': The original value as a float if the status is available, otherwise None.
        """

        response = self.parent.cmd("CALibration:ElECtricity:SCAN?")
        if response:
            parts = response.split(",")
            return {
                "exception_code": parts[0],
                "mode": parts[1],
                "function": parts[2],
                "range": parts[3],
                "status": parts[4],
                "data": float(parts[5]) if parts[4] == "1" else None,
            }
        return {}

    def write_calibration_data(
        self,
        manufacturer_or_user: str,
        password: str,
        channel: int,
        function: int,
        range_: int,
        unit_id: int,
        count: int,
        points: List[float],
        values: List[float],
        year: int,
        month: int,
        day: int,
    ):
        """
        Write calibration data to the device.

        Command:
            CALibration:ElECtricity:DATA <Manufacturer|User>,<password>,<channel>,<function>,<range>,
                                        <unitID>,<count>,<points>,<values>,<year>,<month>,<day>

        Args:
            manufacturer_or_user (str): Specifies factory ("Manufactor") or user calibration ("User").
            password (str): Password for authentication.
            channel (int): Channel number for calibration:
                - 01~02: REF1 and REF2.
                - 101~110: Inner box channels 01A~10A.
                - 111~120: Inner box channels 01B~10B.
                - 201~210: External box 1 channels 01A~10A.
                - 211~220: External box 1 channels 01B~10B.
                Similar ranges apply for external boxes 2 and 3.
            function (int): Function type:
                - 0: Voltage
                - 1: Current
                - 2: Resistance
                - 3: PRT
                - 4: Thermistor
                - 5: CJC
            range_ (int): Range for the selected function:
                - Voltage: 0 (100mV), 1 (1V), 2 (10V), 3 (50V)
                - Current: 0 (100µA), 1 (1mA), 2 (10mA), 3 (100mA)
                - Resistance: 0 (100Ω), 1 (1kΩ), 2 (10kΩ), 3 (100kΩ), 4 (1MΩ), 5 (10MΩ), 6 (100MΩ)
                - PRT: 0 (100Ω), 1 (400Ω), 2 (4kΩ)
                - Thermistor: 0 (0–10kΩ), 1 (10–100kΩ), 2 (0.1–1MΩ)
            unit_id (int): Unit identifier for the calibration.
            count (int): Number of calibration points.
            points (List[float]): Calibration points as a list of floats.
            values (List[float]): Standard values corresponding to calibration points.
            year (int): Calibration year.
            month (int): Calibration month.
            day (int): Calibration day.

        Raises:
            ValueError: If the number of `points` and `values` does not match `count`.

        Returns:
            None
        """
        if len(points) != count or len(values) != count:
            raise ValueError("Number of points and values must match the count")

        points_str = ",".join(map(str, points))
        values_str = ",".join(map(str, values))

        command = (
            f"CALibration:ElECtricity:DATA {manufacturer_or_user},{password},"
            f"{channel},{function},{range_},{unit_id},{count},"
            f'"{points_str}","{values_str}",{year},{month},{day}'
        )
        self.parent.cmd(command)

    def get_calibration_data(
        self,
        manufacturer_or_user: str,
        password: str,
        channel: int,
        function: int,
        range_: int,
    ) -> dict:
        """
        Retrieve calibration data from the device.

        Command:
            CALibration:ElECtricity:DATA? <Manufacturer|User>,<password>,<channel>,<function>,<range>

        Args:
            manufacturer_or_user (str): Specifies whether to retrieve factory ("Manufactor") or user calibration ("User").
            password (str): Password for authentication.
            channel (int): Channel number for calibration:
                - 01~02: REF1 and REF2.
                - 101~110: Inner box channels 01A~10A.
                - 111~120: Inner box channels 01B~10B.
                - 201~210: External box 1 channels 01A~10A.
                - 211~220: External box 1 channels 01B~10B.
                Similar ranges apply for external boxes 2 and 3.
            function (int): Function type:
                - 0: Voltage
                - 1: Current
                - 2: Resistance
                - 3: PRT
                - 4: Thermistor
                - 5: CJC
            range_ (int): Range for the selected function:
                - Voltage: 0 (100mV), 1 (1V), 2 (10V), 3 (50V)
                - Current: 0 (100µA), 1 (1mA), 2 (10mA), 3 (100mA)
                - Resistance: 0 (100Ω), 1 (1kΩ), 2 (10kΩ), 3 (100kΩ), 4 (1MΩ), 5 (10MΩ), 6 (100MΩ)
                - PRT: 0 (100Ω), 1 (400Ω), 2 (4kΩ)
                - Thermistor: 0 (0–10kΩ), 1 (10–100kΩ), 2 (0.1–1MΩ)

        Returns:
            dict: A dictionary containing calibration data with the following keys:
                - "unit_id": Unit identifier.
                - "count": Number of calibration points.
                - "points": List of calibration points.
                - "values": List of standard values.
                - "year": Calibration year.
                - "month": Calibration month.
                - "day": Calibration day.
        """
        command = f"CALibration:ElECtricity:DATA? {manufacturer_or_user},{password},{channel},{function},{range_}"
        response = self.parent.cmd(command)

        if response:
            parts = response.split(",")
            return {
                "unit_id": int(parts[0]),
                "count": int(parts[1]),
                "points": [float(x) for x in parts[2].split(" ")],
                "values": [float(x) for x in parts[3].split(" ")],
                "year": int(parts[4]),
                "month": int(parts[5]),
                "day": int(parts[6]),
            }
        return {}

    def cjcnable(self, enable: bool):
        """
        Enable or disable cold junction calibration.

        Command:
            CALibration:ELECtricity:CJCenable <enable>

        Args:
            enable (bool): Set to True to enable cold junction calibration or False to disable it.

        Returns:
            None
        """

        command = f"CALibration:ELECtricity:CJCenable {int(enable)}"
        self.parent.cmd(command)

    def get_cjc_data(
        self, manufacturer_or_user: str, password: str, location: int, channel: int
    ) -> dict:
        """
        Retrieve cold junction calibration data.

        Command:
            CALibration:ELECtricity:DATA:CJC? <Manufacturer|User>,<password>,<location>,<channel>

        Args:
            manufacturer_or_user (str): Specifies factory ("Manufactor") or user calibration ("User").
            password (str): Authentication password.
            location (int): Calibration location:
                - 1: Internal wiring
                - 0: External wiring
            channel (int): Channel identifier:
                - 101: Embedded location 01A
                - Similar format for other channels.

        Returns:
            dict: A dictionary containing cold junction calibration data with the following keys:
                - "location": Location type (internal or external).
                - "channel": Channel identifier.
                - "data_type": Data type (user or manufacturer).
                - "validity": Whether the data is valid (1 = valid, 0 = invalid).
                - "offset": Calibration offset value.
                - "year": Calibration year.
                - "month": Calibration month.
                - "day": Calibration day.
        """
        command = f"CALibration:ELECtricity:DATA:CJC? {manufacturer_or_user},{password},{location},{channel}"
        response = self.parent.cmd(command)

        if response:
            parts = response.split(",")
            return {
                "location": int(parts[0]),
                "channel": int(parts[1]),
                "data_type": int(parts[2]),
                "validity": int(parts[3]),
                "offset": float(parts[4]),
                "year": int(parts[5]),
                "month": int(parts[6]),
                "day": int(parts[7]),
            }
        return {}

    def write_cjc_data(
        self,
        manufacturer_or_user: str,
        password: str,
        location: int,
        channel: int,
        offset: float,
        year: int,
        month: int,
        day: int,
    ) -> None:
        """
        Write cold junction calibration data.

        Command:
            CALibration:ELECtricity:DATA:CJC <Manufacturer|User>,<password>,<location>,<channel>,<offset>,<year>,<month>,<day>

        Args:
            manufacturer_or_user (str): Specifies factory ("Manufactor") or user calibration ("User").
            password (str): Authentication password.
            location (int): Calibration location:
                - 1: Internal wiring
                - 0: External wiring
            channel (int): Channel identifier (e.g., 101 for embedded position 01A channel).
            offset (float): Calibration offset value.
            year (int): Year of calibration.
            month (int): Month of calibration.
            day (int): Day of calibration.

        Returns:
            None
        """

        command = (
            f"CALibration:ELECtricity:DATA:CJC {manufacturer_or_user},{password},"
            f"{location},{channel},{offset},{year},{month},{day}"
        )
        self.parent.send_command(command)
