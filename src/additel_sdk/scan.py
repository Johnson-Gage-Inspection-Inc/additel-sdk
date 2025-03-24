# scan.py - This file contains the class for the Scan commands.

from .coerce import coerce
from .time import TimeTick
from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
import json
import logging
if TYPE_CHECKING:
    from src.additel_sdk import Additel


def count_decimals(value: float) -> int:
    """Return the number of decimals for a float value."""
    s = str(value)
    return len(s.split(".")[1]) if "." in s else 0

@dataclass
class DIReading:
    ChannelName: str
    Unit: int
    ValuesCount: int = 0
    DateTimeTicks: List[TimeTick] = field(default_factory=list)
    Values: List[float] = field(default_factory=list)
    ValuesFiltered: List[float] = field(default_factory=list)
    ValueDecimals: Optional[int] = None


    def __post_init__(self):
        self.ValuesCount = len(self.Values)
        if self.ValueDecimals is None:
            self.ValueDecimals = count_decimals(self.Values[0])


@dataclass
class DIElectricalReading(DIReading):
    pass


@dataclass
class DITCReading(DIReading):
    NumElectrical: int = 0
    CJCs: List[int] = field(default_factory=list)
    CJCUnit: int = 0
    CjcRaws: List[float] = field(default_factory=list)
    CJCRawsUnit: int = 0
    CJCDecimals: int = 0
    TempValues: List[float] = field(default_factory=list)
    TempUnit: int = 0
    TempDecimals: int = 0


@dataclass
class DITemperatureReading(DIReading):
    """

    Args:
        DIReading (_type_): _description_

    Attributes:
        TempValues (list[float]): List of temperature values.
        TempUnit (int): Temperature unit identifier.
        TempDecimals (int): Number of decimal places for temperature values.
        ValueDecimals (int): the number of decimals from the raw value string

    Returns:
        _type_: _description_
    """
    ChannelName: str
    Unit: int
    ValuesCount: int = 0
    DateTimeTicks: List[datetime] = field(default_factory=list)
    Values: List[float] = field(default_factory=list)
    ValuesFiltered: List[float] = field(default_factory=list)
    TempUnit: int = 0
    TempValuesCount: int = 0
    TempValues: list[float] = field(default_factory=list)
    TempDecimals: Optional[int] = 4  # e.g. usually 4
    ValueDecimals: Optional[int] = None

    @classmethod
    def from_str(cls, input: str) -> "DITemperatureReading":
        dictionaries = []
        for string in input[1:-1].split(";")[:-1]:
            array = string.split(",")
            keys = [f.name for f in fields(cls)[:-1] if f.name != "ValueDecimals"]
            dictionary = dict(zip(keys, array))
            dictionaries.append(dictionary)

        ChannelName = dictionaries[0]["ChannelName"]
        for d in dictionaries:
            d["DateTimeTicks"] = TimeTick.from_ticks(int(d["DateTimeTicks"]))
            d["Values"] = float(d["Values"])
            d["ValuesFiltered"] = float(d["ValuesFiltered"])
            d["TempValues"] = float(d["TempValues"].replace("------", '-inf'))

        assert all(d["ChannelName"] == ChannelName for d in dictionaries), "Mismatched ChannelNames"

        return cls(
            ChannelName=ChannelName,
            Unit=int(dictionaries[0]["Unit"]),
            Values=[d["Values"] for d in dictionaries],
            ValuesFiltered=[d["ValuesFiltered"] for d in dictionaries],
            DateTimeTicks=[d["DateTimeTicks"] for d in dictionaries],
            ValueDecimals=count_decimals(float(dictionaries[0]["Values"])),
            TempUnit=int(dictionaries[0]["TempUnit"]),
            TempDecimals=4,
            TempValues=[d["TempValues"] for d in dictionaries]
        )

    def __str__(self):
        def fmt(val, dec):
            return f"{round(val, dec):.{dec}f}"

        parts = []
        for i in range(len(self.Values)):
            ticks = self.DateTimeTicks[i].to_ticks()
            parts.append(
                f"{self.ChannelName},{self.Unit},1,{ticks},"
                f"{fmt(self.Values[i], self.ValueDecimals)},"
                f"{fmt(self.ValuesFiltered[i], self.ValueDecimals)},"
                f"{self.TempUnit},1,"
                f"{fmt(self.TempValues[i], self.TempDecimals)};"
            )
        return '"' + "".join(parts) + '"'


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

class Scan:
    def __init__(self, parent: "Additel"):
        self.parent = parent

    def start(self, scan_info: DIScanInfo) -> None:
        """Set the configuration and start scanning.

        This command configures the scanning parameters and starts the scan.

        Args:
            params (str): A comma-separated string containing:
                - NPLC (Number of Power Line Cycles)
                - Sample work frequency cycle (100, 1000, or 4000)
                - Channel name
        """
        logging.warning("This command has not been tested.")
        json_params = json.dumps(scan_info.__dict__)
        command = f"JSON:SCAN:STARt {json_params}"
        self.parent.send_command(command)

    def get_configuration_json(self) -> DIScanInfo:
        """Acquire the scanning configuration.

        This command retrieves the current scanning configuration, including:
            - NPLC (Number of Power Line Cycles)
            - The name of the current scanning channel

        Returns:
            str: A comma-separated string containing the scanning configuration:
                - NPLC value
                - Channel name
        """
        if response := self.parent.cmd("JSON:SCAN:STARt?"):
            return coerce(response)

    def get_configuration(self) -> DIScanInfo:
        """Acquire the scanning configuration.

        This command retrieves the current scanning configuration, including:
            - NPLC (Number of Power Line Cycles)
            - The name of the current scanning channel

        Returns:
            str: A comma-separated string containing the scanning configuration:
                - NPLC value
                - Channel name
        """
        response = self.parent.cmd("SCAN:STARt?")
        if response:
            assert response == str(DIScanInfo.from_str(response)), "Unexpected response"
            return DIScanInfo.from_str(response)

    def stop(self) -> None:
        """This command stops any active scanning process on the device."""
        logging.warning("This command has not been tested.")
        self.parent.send_command("SCAN:STOP")

    def get_latest_data(self, longformat=True) -> DIReading:
        """Retrieves the latest scanning data for all active channels.

        Args:
            longformat (bool, optional): Specifies the timestamp format.
                If True, uses long timestamp format (ticks since 1/1/0001)
                If False, uses "yyyy:MM:dd HH:mm:ss fff" format.
                Defaults to False.

        Returns:
            DIReading: An object containing the latest scanning data.
        """
        response = self.parent.cmd(f"SCAN:DATA:Last? {2 if longformat else 1}")
        # FIXME: We're assuming temperature data for now
        instance = DITemperatureReading.from_str(response)
        assert str(instance) == response, "Unexpected response"
        return instance

    def get_data_json(self, count: int = 1) -> DIReading:
        """Acquire scanning data in JSON format.

        This command retrieves scanning data in JSON format for the specified number of
        data points.

        Args:
            count (int): The number of scanning data points to retrieve.

        Returns:
            DIReading: An object containing the scanning data.
        """
        assert count > 0, "Count must be greater than 0."
        if response := self.parent.cmd(f"JSON:SCAN:DATA? {count}"):
            return coerce(response)[0]
        return []

    def get_intelligent_wiring_data_json(
        self, count: int = 1
    ) -> List[DIReading]:  # The response is an empty list :P
        """Acquire scanning data of intelligent wiring (in JSON format).

        Args:
            count (int): The number of scanning data points to retrieve.

        Returns:
            dict: A dictionary representation of the scanning data. Each entry includes:
                - Channel name
                - Electrical measurement data
                - Filtered data
                - Intelligent wiring information
        """
        assert count > 0, "Count must be greater than 0."
        if response := self.parent.cmd(f"JSON:SCAN:SCONnection:DATA? {count}"):
            return coerce(response)
