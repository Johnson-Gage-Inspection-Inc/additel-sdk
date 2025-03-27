# system\communicate\wlan.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.additel_sdk import Additel
import logging


class WLAN:
    def __init__(self, parent: "Additel"):
        self.parent = parent

    # 1.4.10
    def set_state(self, enable: bool) -> None:
        """Set the state of the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN[:STATe] <Boolean>|ON|OFF

        Args:
            enable (bool): Set to True to enable WiFi (ON) or False to disable it (OFF).
        """
        command = f"SYSTem:COMMunicate:SOCKet:WLAN:STATe {int(enable)}"
        self.parent.send_command(command)

    # 1.4.11
    def get_state(self) -> bool:
        """Query the state of the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN[:STATe]?
        Returns:
            bool: True if WiFi is enabled (ON), False if disabled (OFF).
        """
        response = self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:STATe?")
        if response:
            return bool(int(response.strip()))
        raise ValueError("No WiFi state information returned.")

    # 1.4.12
    def set_ip(self, ip_address: str) -> None:
        """Set the IP address for the system's WiFi functionality.

        Design the IP address of WIFI
        Before designing the DHCP、IP subset
        mask and gateway of WIFI, please confirm
        that the wifi module has been opened and
        doesn’t connect with any hot spots.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:ADDRess <ip_address>

        Args:
            ip_address (str): The IP address to set.
        """

        self.parent.System.Communicate.validate_ip(ip_address)
        command = f"SYSTem:COMMunicate:SOCKet:WLAN:ADDRess {ip_address}"
        self.parent.send_command(command)

    # 1.4.13
    def get_ip_address(self) -> str:
        """Query the IP address for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:ADDRess?
        Returns:
            str: The IP address.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:ADDRess?"):
            return response.strip()
        raise ValueError("No IP address information returned.")

    # 1.4.14
    def set_subnet_mask(self, subnet_mask: str) -> None:
        """Set the subnet mask for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:MASK <subnet_mask>

        Args:
            subnet_mask (str): The subnet mask to set.
        """
        self.parent.send_command(f'SYSTem:COMMunicate:SOCKet:WLAN:MASK "{subnet_mask}"')

    # 1.4.15
    def get_subnet_mask(self) -> str:
        """Query the subnet mask for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:MASK?

        Returns:
            str: The subnet mask.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:MASK?"):
            return response.strip()
        raise ValueError("No subnet mask information returned.")

    # 1.4.16
    def set_gateway(self, IPaddress: str) -> None:
        """Set the gateway for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:GATEway <gateway>

        Args:
            IPaddress (str): The gateway to set.
        """
        self.parent.send_command(f"SYSTem:COMMunicate:SOCKet:WLAN:GATEway {IPaddress}")

    # 1.4.17
    def get_gateway(self) -> str:
        """Query the gateway for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:GATEway?

        Returns:
            str: The gateway.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:GATEway?"):
            return response.strip()
        raise ValueError("No gateway information returned.")

    # 1.4.18
    def get_mac(self) -> str:
        """Query the MAC address for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:MAC?

        Returns:
            str: The MAC address.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:MAC?"):
            return response.strip()
        raise ValueError("No MAC address information returned.")

    # 1.4.19
    def set_dhcp(self, enable: bool) -> None:
        """Set the DHCP state for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:DHCP <Boolean>|ON|OFF

        Args:
            enable (bool): Set to True to enable DHCP (ON) or False to disable it (OFF).
        """
        command = f"SYSTem:COMMunicate:SOCKet:WLAN:DHCP {int(enable)}"
        self.parent.send_command(command)

    # 1.4.20
    def get_dhcp(self) -> bool:
        """Query the DHCP state for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:DHCP?

        Returns:
            bool: True if DHCP is open (1), False if closed (0).
        """
        response = self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:DHCP?")
        if response:
            return bool(response.strip())
        raise ValueError("No DHCP state information returned.")

    # 1.4.21
    def set_ssid(self, ssid: str):
        """Set the SSID for the system's WiFi functionality.

        If the parameter is all, the Query will be
        done and all the Queried SSID names and
        the ways of encryption will be returned. If
        the parameter is overlooked, the
        result will return back to the current
        connected SSID name and the ways of
        encryption, if there is no connections or no
        queried hot spots, please return “

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:SSID <ssid>

        Args:
            ssid (str): The SSID to set.

        Returns:
            {[“ssid: way of encryption”]}
        """
        if response := self.parent.cmd(f"SYSTem:COMMunicate:SOCKet:WLAN:SSID {ssid}"):
            return response.strip()
        raise ValueError("No SSID information returned.")

    # 1.4.22
    def connect(self, ssid: str, password: str = None) -> None:
        """Connect to a WiFi network.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:CONNect <ssid>,<password>

        Args:
            ssid (str): hot spot name, the character string with quotation
            password (str, optional): password of the hot spot, the character string

        Returns:
            Successfully,
            Initialization,
            SSIDNotFound
            SSIDNotConfigured,
            JoinFaile
            ScaningConfiguredSSID
            WaitingIPConfiguration
            ModuleJoinedListeningSocke ts
        """
        if password is None:
            command = f"SYSTem:COMMunicate:SOCKet:WLAN:CONNect {ssid}"
        else:
            command = f'SYSTem:COMMunicate:SOCKet:WLAN:CONNect {ssid},"{password}"'
        if response := self.parent.cmd(command):
            logging.info(response.strip())

    # 1.4.23
    def get_connection(self) -> str:
        """Query the connection status of the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:CONNect?

        Returns:
            str: The connection status.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:CONNect?"):
            return response.strip()
        raise ValueError("No connection information returned.")

    # 1.4.24
    def disconnect(self) -> None:
        """Disconnect from the current WiFi network.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:DISConnect
        """
        self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:DISConnect")

    # 1.4.25
    def get_dbm(self):
        """Query signal strength and dBm value of WIFI

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:DBM?
        Returns:
            str: The signal strength and dBm value.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:DBM?"):
            return response.strip()
        raise ValueError("No signal strength information returned.")
