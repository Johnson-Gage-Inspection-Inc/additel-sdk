# scan.py - This file contains the class for the Scan commands.

from typing import List
from .customTypes import DI
import json
from .coerce import coerce

class Scan:
    def __init__(self, parent):
        self.parent = parent

    def start(self, scan_info: DI.DIScanInfo):
        """Set the configuration and start scanning.

        This command configures the scanning parameters and starts the scan.

        Parameters:
            params (str): A comma-separated string containing:
                - NPLC (Number of Power Line Cycles)
                - Sample work frequency cycle (100, 1000, or 4000)
                - Channel name

        Returns:
            None
        """
        raise NotImplementedError("This command is not yet implemented.")
        json_params = json.dumps(scan_info.__dict__)
        command = f'JSON:SCAN:STARt {json_params}'
        self.parent.send_command(command)

    def get_configuration_json(self) -> DI.DIScanInfo:  # Tested!
        """Acquire the scanning configuration.

        This command retrieves the current scanning configuration, including:
            - NPLC (Number of Power Line Cycles)
            - The name of the current scanning channel

        Parameters:
            None

        Returns:
            str: A comma-separated string containing the scanning configuration:
                - NPLC value
                - Channel name
        """
        response = self.parent.send_command("JSON:SCAN:STARt?")
        if response:
            raw_data = json.loads(response)
            dTypes = raw_data.pop('$type').split(',')
            assert 'TAU.Module.Channels.DI.DIScanInfo' in dTypes, "Unexpected type"
            dType = raw_data.pop('ClassName')
            assert dType == 'DIScanInfo', f"Unexpected class name: {dType}"
            return DI.DIScanInfo(**raw_data)

    def get_configuration(self) -> DI.DIScanInfo:  # Tested!
        """Acquire the scanning configuration.

        This command retrieves the current scanning configuration, including:
            - NPLC (Number of Power Line Cycles)
            - The name of the current scanning channel

        Parameters:
            None

        Returns:
            str: A comma-separated string containing the scanning configuration:
                - NPLC value
                - Channel name
        """
        response = self.parent.send_command("SCAN:STARt?")
        if response:
            assert response == DI.DIScanInfo.from_str(response).to_str(), "Unexpected response"
            return DI.DIScanInfo.from_str(response)

    def stop(self):
        """Stop scanning.

        This command stops any active scanning process on the device.

        Parameters:
            None

        Returns:
            None
        """
        raise NotImplementedError("This command is not yet implemented.")
        self.parent.send_command("SCAN:STOP")

    def get_latest_data(self, format=2) -> DI.DIReading:  # Tested!
        """This command retrieves the latest scanning data for all active channels. Optionally, the `time` parameter specifies
        the desired timestamp format:
            - 1: "yyyy:MM:dd HH:mm:ss fff" format
            - 2: Long format (ticks since 1/1/0001)

        Parameters:
            format (int): The desired timestamp format (1: "yyyy:MM:dd HH:mm:ss fff", 2: long format)). Default is 2.

        Returns:
            str: A semicolon-separated string where each entry represents data for a channel. Each entry includes:
                - For Electrical Measurement Data:
                    * Channel name
                    * Electrical unit ID
                    * Number of electrical measurement data
                    * Electrical measurement data
                    * Filtered electrical measurement data
                - For Temperature Data:
                    * Channel name
                    * Electrical unit ID
                    * Number of electrical measurement data
                    * Electrical measurement data
                    * Filtered electrical measurement data
                    * Indication unit ID
                    * Number of indication data
                    * Indication data
                - For TC Data:
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
        response = self.parent.send_command(f"SCAN:DATA:Last? {format}")
        return DI.DIReading.from_str(response)

    def get_scan_data_json(self, count: int = 1) -> List[DI.DIReading]:  # Tested!
        """Acquire scanning data in JSON format.

        This command retrieves scanning data in JSON format for the specified number of data points.

        Parameters:
            count (int): The number of scanning data points to retrieve.

        Returns:
            dict: A dictionary representation of the scanning data. Each entry includes:
                - Channel name
                - Electrical measurement data
                - Filtered data
                - Additional parameters depending on the measurement type
        """
        assert count > 0, "Count must be greater than 0."
        if response := self.parent.send_command(f"JSON:SCAN:DATA? {count}"):
            return coerce(response)
        return []
