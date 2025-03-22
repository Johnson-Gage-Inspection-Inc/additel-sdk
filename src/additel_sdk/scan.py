# scan.py - This file contains the class for the Scan commands.

from dataclasses import dataclass, field
from typing import List
import json
from .coerce import coerce
import logging
from datetime import datetime, timedelta
from math import inf


@dataclass
class DIReading:
    ChannelName: str = ""
    Unit: int = 0
    Values: List[float] = field(default_factory=list)
    ValuesFiltered: List[float] = field(default_factory=list)
    DateTimeTicks: List[datetime] = field(default_factory=list)
    ValueDecimals: int = 0


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
    def __init__(self, parent):
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

        Args:
            None

        Returns:
            str: A comma-separated string containing the scanning configuration:
                - NPLC value
                - Channel name
        """
        response = self.parent.cmd("JSON:SCAN:STARt?")
        if response:
            raw_data = json.loads(response)
            dTypes = raw_data.pop("$type").split(",")
            assert "TAU.Module.Channels.DI.DIScanInfo" in dTypes, "Unexpected type"
            dType = raw_data.pop("ClassName")
            assert dType == "DIScanInfo", f"Unexpected class name: {dType}"
            return DIScanInfo(**raw_data)

    def get_configuration(self) -> DIScanInfo:
        """Acquire the scanning configuration.

        This command retrieves the current scanning configuration, including:
            - NPLC (Number of Power Line Cycles)
            - The name of the current scanning channel

        Args:
            None

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
        return DITemperatureReading.from_str(response)

    def get_data_json(self, count: int = 1) -> DIReading:
        """Acquire scanning data in JSON format.

        This command retrieves scanning data in JSON format for the specified number of data points.

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


def ticks_to_datetime(ticks):
    return datetime(1, 1, 1) + timedelta(seconds=int(ticks) / 10_000_000)


def datetime_to_ticks(dt):
    return (dt - datetime(1, 1, 1)) / timedelta(seconds=1) * 10_000_000


@dataclass
class DITemperatureReading(DIReading):
    TempValues: list[float] = field(default_factory=list)
    TempUnit: int = 0
    TempDecimals: int = 0  # e.g. usually 4

    @classmethod
    def from_str(cls, input: str) -> "DITemperatureReading":
        dictionaries = []
        # Remove the surrounding quotes, split by ";" and ignore trailing empty element.
        for string in input[1:-1].split(";")[:-1]:
            array = string.split(",")
            # Define keys for the expected ordering:
            keys = [
                "ChannelName", "Unit", "ValuesCount", "DateTimeTicks",
                "Values", "ValuesFiltered", "TempUnit", "TempValuesCount", "TempValues"
            ]
            dictionary = dict(zip(keys, array))
            # Compute the number of decimals from the raw value string; this is ValueDecimals.
            dictionary["ValueDecimals"] = len(str(array[4]).split(".")[1])
            dictionaries.append(dictionary)

        ChannelName = dictionaries[0]["ChannelName"]
        for d in dictionaries:
            d["DateTimeTicks"] = ticks_to_datetime(d["DateTimeTicks"])
            d["Values"] = float(d["Values"])
            d["ValuesFiltered"] = float(d["ValuesFiltered"])
            d["TempValues"] = -inf if d["TempValues"] == "------" else float(d["TempValues"])

        assert all(d["ChannelName"] == ChannelName for d in dictionaries), "Mismatched ChannelNames"

        instance = cls(
            ChannelName=ChannelName,
            Unit=int(dictionaries[0]["Unit"]),
            Values=[d["Values"] for d in dictionaries],
            ValuesFiltered=[d["ValuesFiltered"] for d in dictionaries],
            DateTimeTicks=[d["DateTimeTicks"] for d in dictionaries],
            ValueDecimals=int(dictionaries[0]["ValueDecimals"]),
            TempUnit=int(dictionaries[0]["TempUnit"]),
            # Here we assume TempDecimals is fixed at 4 (or you could derive it from elsewhere)
            TempDecimals=4,
            TempValues=[d["TempValues"] for d in dictionaries]
        )
        return instance

    def __str__(self):
        def fmt(val, dec):
            return f"{round(val, dec):.{dec}f}"

        parts = []
        for i in range(len(self.Values)):
            dt_ticks = int(datetime_to_ticks(self.DateTimeTicks[i]) / 1000) * 1000
            parts.append(
                f"{self.ChannelName},{self.Unit},1,{dt_ticks},"
                f"{fmt(self.Values[i], self.ValueDecimals)},"
                f"{fmt(self.ValuesFiltered[i], self.ValueDecimals)},"
                f"{self.TempUnit},1,"
                f"{fmt(self.TempValues[i], self.TempDecimals)};"
            )
        # Return the complete string wrapped in quotes
        return '"' + "".join(parts) + '"'

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
