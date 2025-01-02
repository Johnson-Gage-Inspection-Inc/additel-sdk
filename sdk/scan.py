# scan.py - This file contains the class for the Scan commands.

from typing import List, Optional
from .customTypes import type
import json

class Scan:
    def __init__(self, parent):
        self.parent = parent

    def start(self, scan_info: type.DIScanInfo):
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
        json_params = json.dumps(scan_info.__dict__)
        command = f'JSON:SCAN:STARt {json_params}'
        self.parent.send_command(command)

    def get_configuration(self) -> type.DIScanInfo:
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
            return type.DIScanInfo(**json.loads(response))
        return None

    def stop(self):
        """Stop scanning.

        This command stops any active scanning process on the device.

        Parameters:
            None

        Returns:
            None
        """
        self.parent.send_command("SCAN:STOP")

    def get_latest_data(self, time_format: Optional[str] = None) -> Optional[str]:
        """Acquire the most recent scanning data.

        This command retrieves the latest scanning data for all active channels. Optionally, the `time` parameter specifies
        the desired timestamp format:
            - 1: "yyyy:MM:dd HH:mm:ss fff" format
            - 2: Long format

        Parameters:
            time (str, optional): Timestamp format. Defaults to an empty string, indicating no specific time format.

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
        command = "SCAN:DATA:Last?"
        if time_format:
            command += f" {time_format}"
        return self.parent.send_command(command)

    def get_data_json(self, count: int) -> List[dict]:
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
        command = f"JSON:SCAN:DATA? {count}"
        response = self.parent.send_command(command)
        if response:
            return json.loads(response)
        return []
