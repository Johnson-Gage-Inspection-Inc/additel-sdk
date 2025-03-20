# scan.py - This file contains the class for the Scan commands.

from typing import List
import json
from .coerce import coerce
import logging
from datetime import datetime, timedelta
from math import inf


class DIReading:
    """Represents a single channel's measurement data."""

    def __init__(self, **kwargs):
        self.ChannelName = kwargs.pop("ChannelName", "")
        self.Unit: int = kwargs.pop("Unit", 0)
        self.Values: List[float] = kwargs.pop("Values", [])
        self.ValuesFiltered: List[float] = kwargs.pop("ValuesFiltered", [])
        self.DateTimeTicks: List[datetime] = kwargs.pop("DateTimeTicks", [])
        self.ValueDecimals: int = kwargs.pop("ValueDecimals", 0)
        if kwargs:
            logging.warning(f"Unhandled keys: {kwargs.keys()}")
        try:
            if kwargs.pop("ClassName", None):
                self.validate_structure(kwargs)
            self.__dict__.update(kwargs)
        except Exception as e:
            print(f"Error: {e}")

    def validate_structure(self, kwargs={}):
        # If there are extra keys that haven't been handled by the subclass,
        # you can either ignore them or raise an error.
        if kwargs:
            raise ValueError(f"Unexpected keys: {list(kwargs.keys())}")

        # Make sure no values are null
        for key, value in self.__dict__.items():
            if not value:
                raise ValueError(f"Value for {key} is null")

    @staticmethod
    def ticksToDatetime(ticks):
        return datetime(1, 1, 1) + timedelta(seconds=int(ticks) / 10_000_000)

    @staticmethod
    def datetimeToTicks(dt):
        return (dt - datetime(1, 1, 1)) / timedelta(seconds=1) * 10_000_000


class DIScanInfo(dict):
    """Data structure for scanning information.

    Each configuration includes:
        NPLC (int): Number of Power Line Cycles (NPLC).
        ChannelName (int): Sampling frequency cycle.
        ClassName
    """

    def __init__(self, NPLC: int, ChannelName: str):
        self["NPLC"] = NPLC  # Number of Power Line Cycles (NPLC)
        self["ChannelName"] = ChannelName  # Sampling frequency cycle

    @classmethod
    def from_str(cls, data: str):
        """Parse the scanning information from a string.

        Args:
            data (str): A comma-separated list of length 2, containing the scan information.

        Returns:
            DIScanInfo: An instance of DIScanInfo populated with the string data.
        """
        NPLC, ChannelName = data.split(",")
        return cls(NPLC=int(NPLC), ChannelName=str(ChannelName))

    def __str__(self):
        """Convert the DIScanInfo object to a string representation."""
        return f"{self['NPLC']},{self['ChannelName']}"


class Scan:
    def __init__(self, parent):
        self.parent = parent

    def start(self, scan_info: DIScanInfo):
        """Set the configuration and start scanning.

        This command configures the scanning parameters and starts the scan.

        Args:
            params (str): A comma-separated string containing:
                - NPLC (Number of Power Line Cycles)
                - Sample work frequency cycle (100, 1000, or 4000)
                - Channel name

        Returns:
            None
        """
        logging.warning("This command has not been tested.")
        json_params = json.dumps(scan_info.__dict__)
        command = f"JSON:SCAN:STARt {json_params}"
        self.parent.cmd(command)

    def get_configuration_json(self) -> DIScanInfo:  # Tested!
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

    def get_configuration(self) -> DIScanInfo:  # Tested!
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

    def stop(self):
        """Stop scanning.

        This command stops any active scanning process on the device.

        Args:
            None

        Returns:
            None
        """
        logging.warning("This command has not been tested.")
        self.parent.cmd("SCAN:STOP")

    def get_latest_data(self, format=2) -> DIReading:  # Tested!
        """This command retrieves the latest scanning data for all active channels. Optionally, the `time` parameter specifies
        the desired timestamp format:
            - 1: "yyyy:MM:dd HH:mm:ss fff" format
            - 2: Long format (ticks since 1/1/0001)

        Args:
            format (int): The desired timestamp format (1: "yyyy:MM:dd HH:mm:ss fff", 2: long format)). Default is 2.

        Returns:
            str: A semicolon-separated string where each entry represents data for a channel. Each entry includes:
                - For Switch Data:
                    * Status data (based on TC or RTD data)
                - For Voltage/Current Transmitter Data:
                    * Channel name
                    * Electrical unit ID
                    * Number of electrical measurement data
                    * Electrical measurement data
                    * Filtered electrical measurement data
                    * Input signal unit ID
                    * Input signal name
                    * Number of input signals
                    * Input signal data
        """
        if format not in [1, 2]:
            raise ValueError("Invalid format. Must be 1 or 2.")
        if format == 1:
            raise NotImplementedError("This format is not implemented.")
        response = self.parent.cmd(f"SCAN:DATA:Last? {format}")
        # FIXME: We're assuming temperature data for now
        return DITemperatureReading.from_str(response)

    def get_data_json(self, count: int = 1) -> DIReading:  # Tested!
        """Acquire scanning data in JSON format.

        This command retrieves scanning data in JSON format for the specified number of data points.

        Args:
            count (int): The number of scanning data points to retrieve.

        Returns:
            dict: A dictionary representation of the scanning data. Each entry includes:
                - Channel name
                - Electrical measurement data
                - Filtered data
                - Additional parameters depending on the measurement type
        """
        assert count > 0, "Count must be greater than 0."
        if response := self.parent.cmd(f"JSON:SCAN:DATA? {count}"):
            return coerce(response)[0]
        return []

    def get_intelligent_wiring_data_json(
        self, count: int = 1
    ) -> List[DIReading]:  # Tested! But the response is an empty list :P
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


class DITemperatureReading(DIReading):
    """Represents a single channel's temperature measurement data.

    Args:
        DIReading: The base class for all DI readings. Includes:
            * Channel name
            * Electrical unit ID
            * Number of electrical measurement data
            * Electrical measurement data
            * Filtered electrical measurement data
            * Indication unit ID
            * Number of indication data
            * Indication data
    """

    def __init__(self, **kwargs):
        self.TempValues: List[float] = kwargs.pop("TempValues", [])
        self.TempUnit: int = kwargs.pop("TempUnit", 0)
        self.TempDecimals: int = kwargs.pop("TempDecimals", 0)
        # Ensure the ClassName is correctly set for validation
        kwargs.setdefault("ClassName", "TAU.Module.Channels.DI.DITemperatureReading")
        super().__init__(**kwargs)

    @classmethod
    def from_str(self, input: str):
        dictionaries = []
        for string in input[1:-1].split(";")[0:-1]:
            # if string starts and ends with double quotes, remove them
            array = string.split(",")
            keys = [
                "ChannelName",
                "Unit",
                "?",
                "DateTimeTicks",
                "Values",
                "ValuesFiltered",
                "TempUnit",
                "?",  # TempDecimals?
                "TempValues",
            ]
            dictionary = dict(zip(keys, array))
            dictionary["TempDecimals"] = len(str(array[4]).split(".")[1])
            dictionaries.append(dictionary)

        ChannelName = dictionary["ChannelName"]
        dictionary["DateTimeTicks"] = [
            self.ticksToDatetime(d["DateTimeTicks"]) for d in dictionaries
        ]
        dictionary["Values"] = [float(d["Values"]) for d in dictionaries]
        dictionary["ValuesFiltered"] = [
            float(d["ValuesFiltered"]) for d in dictionaries
        ]

        def extendedFloat(x) -> float:
            if x == '------':
                return -inf
            return float(x)

        dictionary["TempValues"] = [extendedFloat(d["TempValues"]) for d in dictionaries]

        assert all(
            dictionaries[i]["ChannelName"] == dictionaries[i + 1]["ChannelName"]
            for i in range(len(dictionaries) - 1)
        ), "Channel names do not match"
        assert all(
            dictionaries[i]["Unit"] == dictionaries[i + 1]["Unit"]
            for i in range(len(dictionaries) - 1)
        ), f"Units do not match for channel {ChannelName}: {[dictionaries[i]['Unit'] for i in range(len(dictionaries))]}"
        assert all(
            dictionaries[i]["TempUnit"] == dictionaries[i + 1]["TempUnit"]
            for i in range(len(dictionaries) - 1)
        ), f"Temperature units do not match for channel {ChannelName}"
        assert all(
            dictionaries[i]["TempDecimals"] == dictionaries[i + 1]["TempDecimals"]
            for i in range(len(dictionaries) - 1)
        ), f"Temperature decimals do not match for channel {ChannelName}"
        assert (
            len(dictionary["Values"])
            == len(dictionary["ValuesFiltered"])
            == len(dictionary["TempValues"])
            == len(dictionary["DateTimeTicks"])
        ), f"Lengths of data do not match for channel {ChannelName}"

        return self(**dictionary)

    def __str__(self):
        def rnd(li: list, n: int = None) -> List[float]:
            if not n:
                n = self.TempDecimals
            return [f"{round(float(x), n):.{n}f}" for x in li]

        DateTimeTicks = [
            int(self.datetimeToTicks(x) / 1000) * 1000 for x in self.DateTimeTicks
        ]
        Values = rnd(self.Values)
        ValuesFiltered = rnd(self.ValuesFiltered)
        TempValues = rnd(self.TempValues, 4)
        output = ""
        n = len(self.Values)
        for i in range(n):
            output += f"{self.ChannelName},{self.Unit},1,{DateTimeTicks[i]},{Values[i]},{ValuesFiltered[i]},{self.TempUnit},1,{TempValues[i]};"
        return f'"{output}"'

    def __repr__(self):
        return str(self)


class DIElectricalReading(DIReading):
    """Represents a single channel's electrical measurement data.

    Args:
        DIReading: The base class for all DI readings. Includes:                - For Electrical Measurement Data:
            * Channel name
            * Electrical unit ID
            * Number of electrical measurement data
            * Electrical measurement data
            * Filtered electrical measurement data
    """

    def __init__(self, **kwargs):
        logging.warning("DIElectricalReading.__init__() has not been tested.")
        kwargs.setdefault("ClassName", "TAU.Module.Channels.DI.DIElectricalReading")
        super().__init__(**kwargs)


class DITCReading(DIReading):
    """Represents a single channel's thermocouple measurement data.

    Args:
        DIReading: The base class for all DI readings. Includes:
            * Channel name
            * Electrical unit ID
            * Number of electrical measurement data
            * Electrical measurement data
            * Filtered electrical measurement data
            * Indication unit ID
            * Number of indication data
            * Indication data
            * Cold junction electrical unit ID
            * Cold junction electrical test data
            * Cold junction temperature unit ID
            * Cold junction temperature data

        TC data:
            Channel name
            Electrical unit Id
            Number of electrical measurement data 1 electrical measurement data
            electrical measurement data after filter Indication unit Id
            Number of indication data 1 the indication data
            Cold junction electrical unitId
            Cold junction electrical measurement data number 1
            cold junction electrical test data
            Cold junction temperature unit Id
            Cold junction temperature data number 1
            cold junction temperature data
    """

    def __init__(self, **kwargs):
        logging.warning("DITCReading.__init__() has not been tested.")
        # For the electrical measurement part, we can add a count if desired.
        self.NumElectrical: int = kwargs.pop(
            "NumElectrical", len(kwargs.get("Values", []))
        )
        # Additional TC-specific fields:
        self.IndicationUnit: int = kwargs.pop("IndicationUnit", 0)
        self.NumIndication: int = kwargs.pop("NumIndication", 0)
        self.IndicationData: list[float] = kwargs.pop("IndicationData", [])
        self.CJElectricalUnit: int = kwargs.pop("CJElectricalUnit", 0)
        self.NumCJElectrical: int = kwargs.pop("NumCJElectrical", 0)
        self.CJElectricalTest: float = kwargs.pop("CJElectricalTest", 0.0)
        self.CJTemperatureUnit: int = kwargs.pop("CJTemperatureUnit", 0)
        self.NumCJTemperature: int = kwargs.pop("NumCJTemperature", 0)
        self.CJTemperatureData: list[float] = kwargs.pop("CJTemperatureData", [])
        # Set the proper ClassName for later coercion.
        kwargs.setdefault("ClassName", "TAU.Module.Channels.DI.DITCReading")
        super().__init__(**kwargs)
