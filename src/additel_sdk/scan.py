# scan.py - This file contains the class for the Scan commands.

from .channel import Channel
from .coerce import coerce
from .registry import register_type
from .time import TimeTick
from contextlib import contextmanager
from dataclasses import dataclass, field, fields
from time import sleep
from typing import TYPE_CHECKING, Optional, List, get_origin, get_args
import logging

if TYPE_CHECKING:
    from src.additel_sdk import Additel


def count_decimals_str(value: str) -> int:
    if '.' in value:
        return len(value.split('.')[1].rstrip('\n').rstrip())
    return 0


@register_type("TAU.Module.Channels.DI.DIReading")
@dataclass
class DIReading:
    ChannelName: str
    Unit: int
    ValuesCount: int = 0
    DateTimeTicks: List[TimeTick] = field(default_factory=list)
    Values: List[float] = field(default_factory=list)
    ValuesFiltered: List[float] = field(default_factory=list)
    ValueDecimals: Optional[int] = 6

    def __post_init__(self):
        self._post_init_common()

    def _post_init_common(self):
        self.ValuesCount = len(self.Values)
        assert self.ChannelName in Channel.valid_names, "Invalid channel name"

    def __eq__(self, other):
        return str(self) == str(other)


@register_type("TAU.Module.Channels.DI.DIElectricalReading")
@dataclass
class DIElectricalReading(DIReading):
    pass


@register_type("TAU.Module.Channels.DI.DITCReading")
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


@register_type("TAU.Module.Channels.DI.DITemperatureReading")
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

    TempUnit: int = 0
    TempValuesCount: int = 0
    TempValues: list[float] = field(default_factory=list)
    TempDecimals: Optional[int] = 4  # e.g. usually 4

    def __post_init__(self):
        super()._post_init_common()
        self.TempValuesCount = len(self.TempValues)

    @classmethod
    def from_str(cls, input: str) -> "DITemperatureReading":
        treated_input = input[1:-2].replace("------", "-inf")
        array = [reading.split(",") for reading in treated_input.split(";")]
        transposed = list(map(list, zip(*array)))

        # Prepare initial mapping
        values = {}

        # Use these to find decimals from raw values
        raw_value_strs = transposed[4]  # Values
        raw_temp_strs = transposed[8]  # TempValues

        # Parse all the fields like before
        fs = [f for f in fields(cls)[:-1] if f.name != "ValueDecimals"]
        for i, f in enumerate(fs):
            if get_origin(f.type) is list:
                (type_,) = get_args(f.type)
                values[f.name] = [type_(v) for v in transposed[i]]
            else:
                first_value = f.type(transposed[i][0])
                if values.get(f.name) is None:
                    values[f.name] = first_value if transposed[i] else None
                else:
                    assert values[f.name] == first_value, "Unexpected type"

        # Extract decimal counts from raw strings
        values["ValueDecimals"] = count_decimals_str(raw_value_strs[0])
        values["TempDecimals"] = count_decimals_str(raw_temp_strs[0])

        return cls(**values)

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


@register_type("TAU.Module.Channels.DI.DIScanInfo")
@dataclass
class DIScanInfo:
    NPLC: int
    ChannelName: str

    def __post_init__(self):
        Channel.validate_name(self.ChannelName)

    @classmethod
    def from_str(cls, data: str) -> "DIScanInfo":
        """Parse the scanning information from a string."""
        NPLC, ChannelName = data.split(",")
        return cls(NPLC=int(NPLC), ChannelName=ChannelName)

    def __str__(self) -> str:
        """Convert the DIScanInfo object to a string representation."""
        return f"{self.NPLC},{self.ChannelName}"
    
    def __dict__(self) -> dict:
        return {
            "$type": "TAU.Module.Channels.DI.DIScanInfo, TAU.Module.Channels",
            "ChannelName": self.ChannelName,
            "NPLC": self.NPLC,
            "ClassName": "DIScanInfo"
        }


class Scan:
    def __init__(self, parent: "Additel"):
        self.parent = parent

    def start(self, scan_info: DIScanInfo) -> None:
        """Set the configuration and start scanning.

        This command configures the scanning parameters and starts the scan.

        Args:
            scan_info (DIScanInfo): The scanning configuration.
        """
        logging.warning("This command has not been tested.")
        command = f"JSON:SCAN:STARt {scan_info}"
        self.parent.send_command(command)

    def get_configuration_json(self, measure=False) -> DIScanInfo:
        """Acquire the scanning configuration.

        This command retrieves the current scanning configuration, including:
            - NPLC (Number of Power Line Cycles)
            - The name of the current scanning channel

        Returns:
            DIScanInfo: An object containing the scanning configuration.
        """
        meas = "MEASure:" if measure else ""
        if response := self.parent.cmd(meas + "JSON:SCAN:STARt?"):
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

    def stop(self, measure=False) -> None:
        """This command stops any active scanning process on the device."""
        logging.warning("This command has not been tested.")
        meas = "MEASure:" if measure else ""
        self.parent.send_command(f"{meas}SCAN:STOP")

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

    def get_data_json(self, count: int = 1) -> List[DIReading]:
        """Acquire scanning data in JSON format.

        This command retrieves scanning data in JSON format for the specified number of
        data points.

        Args:
            count (int): The number of scanning data points to retrieve, per channel.

        Returns:
            DIReading: An object containing the scanning data.
        """
        assert count > 0, "Count must be greater than 0."
        if response := self.parent.cmd(f"JSON:SCAN:DATA? {count}"):
            return coerce(response)

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

    def start_multi_channel_scan(
        self, channel_list: List[str], sampling_rate: int = 1000, measure: bool = False
    ) -> None:
        """Start scanning for multiple channels.

        Args:
            sampling_rate (int): The sampling rate in ms (e.g., 1000).
            channel_list (List[str]): List of channel names.
        """
        meas = "MEASure:" if measure else ""
        channels = ",".join(channel_list)
        command = f'{meas}SCAN:MULT:STARt {sampling_rate},"{channels}"'
        self.parent.send_command(command)
        sleep(sampling_rate / 1000)  # Wait for one cycle

    @contextmanager
    def preserve_scan_state(self):
        original = self.get_configuration()
        try:
            yield
        finally:
            self.start(original)

    def get_readings(self, desired_channels: List[str]) -> List["DIReading"]:
        """Start a multi-channel scan and return the last reading from each specified
        channel.

        Args:
            desired_channels (List[str]): List of channel names to scan.

        Returns:
            List[DIReading]: A list of readings, one per channel.
        """
        with self.preserve_scan_state():
            self.stop()
            self.start_multi_channel_scan(desired_channels)
            return self.get_data_json()
