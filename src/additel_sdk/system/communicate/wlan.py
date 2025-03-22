# system\communicate\wlan.py


class WLAN:
    def __init__(self, parent):
        self.parent = parent

    # 1.4.10
    def setstate(self, enable: bool):
        """
        Set the state of the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN[:STATe] <Boolean>|ON|OFF

        Args:
            enable (bool): Set to True to enable WiFi (ON) or False to disable it (OFF).

        Returns:
            None
        """
        command = f"SYSTem:COMMunicate:SOCKet:WLAN:STATe {int(enable)}"
        self.parent.cmd(command)

    # 1.4.11
    def getstate(self) -> bool:
        """
        Query the state of the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN[:STATe]?

        Args:
            None

        Returns:
            bool: True if WiFi is enabled (ON), False if disabled (OFF).
        """
        response = self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:STATe?")
        if response:
            return bool(response.strip())
        raise ValueError("No WiFi state information returned.")

    # 1.4.12
    def set_wlan_ip_address(self, ip_address: str):
        """
        Set the IP address for the system's WiFi functionality.

        Design the IP address of WIFI
        Before designing the DHCP、IP subset
        mask and gateway of WIFI, please confirm
        that the wifi module has been opened and
        doesn’t connect with any hot spots.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:ADDRess <ip_address>

        Args:
            ip_address (str): The IP address to set.

        Returns:
            None
        """
        # FIXME: Validate IP address format
        command = f"SYSTem:COMMunicate:SOCKet:WLAN:ADDRess {ip_address}"
        self.parent.cmd(command)

    # 1.4.13
    def get_ip_address(self) -> str:
        """
        Query the IP address for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:ADDRess?

        Args:
            None

        Returns:
            str: The IP address.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:ADDRess?"):
            return response.strip()
        raise ValueError("No IP address information returned.")

    # 1.4.14
    def set_subnet_mask(self, subnet_mask: str):
        """
        Set the subnet mask for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:MASK <subnet_mask>

        Args:
            subnet_mask (str): The subnet mask to set.

        Returns:
            None
        """
        if response := self.parent.cmd(
            f"SYSTem:COMMunicate:SOCKet:WLAN:MASK {subnet_mask}"
        ):
            return response.strip()
        raise ValueError("No subnet mask information returned.")

    # 1.4.15
    def get_subnet_mask(self) -> str:
        """
        Query the subnet mask for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:MASK?

        Args:
            None

        Returns:
            str: The subnet mask.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:MASK?"):
            return response.strip()
        raise ValueError("No subnet mask information returned.")

    # 1.4.16
    def setGateway(self, IPaddress: str):
        """
        Set the gateway for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:GATEway <gateway>

        Args:
            IPaddress (str): The gateway to set.

        Returns:
            None
        """
        if response := self.parent.cmd(
            f"SYSTem:COMMunicate:SOCKet:WLAN:GATEway {IPaddress}"
        ):
            return response.strip()
        raise ValueError("No gateway information returned.")

    # 1.4.17
    def getGateway(self) -> str:
        """
        Query the gateway for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:GATEway?

        Args:
            None

        Returns:
            str: The gateway.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:GATEway?"):
            return response.strip()
        raise ValueError("No gateway information returned.")

    # 1.4.18
    def getMAC(self) -> str:
        """
        Query the MAC address for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:MAC?

        Args:
            None

        Returns:
            str: The MAC address.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:MAC?"):
            return response.strip()
        raise ValueError("No MAC address information returned.")

    # 1.4.19
    def setDHCP(self, enable: bool):
        """
        Set the DHCP state for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:DHCP <Boolean>|ON|OFF

        Args:
            enable (bool): Set to True to enable DHCP (ON) or False to disable it (OFF).

        Returns:
            None
        """
        command = f"SYSTem:COMMunicate:SOCKet:WLAN:DHCP {int(enable)}"
        self.parent.cmd(command)

    # 1.4.20
    def getDHCP(self) -> bool:
        """
        Query the DHCP state for the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:DHCP?

        Args:
            None

        Returns:
            bool: True if DHCP is open (1), False if closed (0).
        """
        response = self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:DHCP?")
        if response:
            return bool(response.strip())
        raise ValueError("No DHCP state information returned.")

    # 1.4.21
    def setSSID(self, ssid: str):
        """
        Set the SSID for the system's WiFi functionality.

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
    def connect(self, ssid: str, password: str):
        """
        Connect to a WiFi network.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:CONNect <ssid>,<password>

        Args:
            ssid (str): hot spot name, the character string with quotation
            encryptionMode, WEP_OFF, WEP_ON, WEP_AUTO, WPA_PSK, WPA_TKIP, WPA2_PSK, WPA2_AES,CCKM_TKIP, WEP_CKIP, WEP_AUTO_CKIP, CCKM_AES, WPA_PSK_AES, WPA_AES, WPA2_PSK_TKIP, WPA2_TKIP, WAPI_PSK, WAPI_CERT
            password (str): The password for the WiFi network, the character string with quotation

        Returns:
            None
        """
        command = f"SYSTem:COMMunicate:SOCKet:WLAN:CONNect {ssid},{password}"
        self.parent.cmd(command)

    # 1.4.23
    def getConnection(self) -> str:
        """
        Query the connection status of the system's WiFi functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:CONNect?

        Args:
            None

        Returns:
            str: The connection status.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:CONNect?"):
            return response.strip()
        raise ValueError("No connection information returned.")

    # 1.4.24
    def disconnect(self):
        """
        Disconnect from the current WiFi network.

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:DISConnect

        Args:
            None

        Returns:
            None
        """
        self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:DISConnect")

    # 1.4.25
    def getDBM(self):
        """Query signal strength and dBm value of WIFI

        Command:
            SYSTem:COMMunicate:SOCKet:WLAN:DBM?

        Args:
            None

        Returns:
            str: The signal strength and dBm value.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:WLAN:DBM?"):
            return response.strip()
        raise ValueError("No signal strength information returned.")
