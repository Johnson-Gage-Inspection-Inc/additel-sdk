# scan.py - This file contains the class for the Scan commands.

from .coerce import coerce
from .channel import DI
from typing import TYPE_CHECKING, List
import json
import logging
if TYPE_CHECKING:
    from src.additel_sdk import Additel

class Scan:
    def __init__(self, parent: "Additel"):
        self.parent = parent

    def start(self, scan_info: DI.DIScanInfo) -> None:
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

    def get_configuration_json(self) -> DI.DIScanInfo:
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

    def get_configuration(self) -> DI.DIScanInfo:
        """Acquire the scanning configuration.

        This command retrieves the current scanning configuration, including:
            - NPLC (Number of Power Line Cycles)
            - The name of the current scanning channel

        Returns:
            str: A comma-separated string containing the scanning configuration:
                - NPLC value
                - Channel name
        """        
        if response := self.parent.cmd("SCAN:STARt?"):
            configuration_info = DI.DIScanInfo.from_str(response)
            assert response == str(configuration_info), "Unexpected response"
            return configuration_info

    def stop(self) -> None:
        """This command stops any active scanning process on the device."""
        logging.warning("This command has not been tested.")
        self.parent.send_command("SCAN:STOP")

    def get_latest_data(self, longformat=True) -> DI.DIReading:
        """Retrieves the latest scanning data for all active channels.

        Args:
            longformat (bool, optional): Specifies the timestamp format.
                If True, uses long timestamp format (ticks since 1/1/0001)
                If False, uses "yyyy:MM:dd HH:mm:ss fff" format.
                Defaults to False.

        Returns:
            DI.DIReading: An object containing the latest scanning data.
        """
        response = self.parent.cmd(f"SCAN:DATA:Last? {2 if longformat else 1}")
        # FIXME: We're assuming temperature data for now
        instance = DI.DITemperatureReading.from_str(response)
        assert str(instance) == response, "Unexpected response"
        return instance

    def get_data_json(self, count: int = 1) -> DI.DIReading:
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
    ) -> List[DI.DIReading]:  # The response is an empty list :P
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
