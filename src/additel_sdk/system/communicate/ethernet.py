# system\communicate\ethernet.py
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.additel_sdk.system.communicate import Communicate


class Ethernet:
    def __init__(self, parent: "Communicate"):
        self.parent = parent

    # 1.4.26
    def getDHCP(self) -> bool:
        """Query the DHCP state for the system's Ethernet functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:ETHernet:DHCP?
        Returns:
            bool: True if DHCP is open (1), False if closed (0).
        """
        response = self.parent.cmd("SYSTem:COMMunicate:SOCKet:ETHernet:DHCP?")
        if response:
            return bool(response.strip())
        raise ValueError("No DHCP state information returned.")

    # 1.4.27
    def setDHCP(self, enable: bool) -> None:
        """Set the DHCP state for the system's Ethernet functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:ETHernet:DHCP <Boolean>|ON|OFF

        Args:
            enable (bool): Set to True to enable DHCP (ON) or False to disable it (OFF).
        """
        command = f"SYSTem:COMMunicate:SOCKet:ETHernet:DHCP {int(enable)}"
        self.parent.cmd(command)

    # 1.4.28
    def getIP(self) -> str:
        """Query the IP address for the system's Ethernet functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:ETHernet:ADDRess?
        Returns:
            str: The IP address.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:ETHernet:ADDRess?"):
            return response.strip()
        raise ValueError("No IP address information returned.")

    # 1.4.29
    def set_ip(self, ip_address: str) -> None:
        """Set the IP address for the system's Ethernet functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:ETHernet:ADDRess <ip_address>

        Args:
            ip_address (str): The IP address to set.
        """
        self.parent.validate_ip(ip_address)
        self.parent.cmd(
            f"SYSTem:COMMunicate:SOCKet:ETHernet:ADDRess {ip_address}"
        )

    # 1.4.30
    def getMASK(self) -> str:
        """Query the subnet mask for the system's Ethernet functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:ETHernet:MASK?

        Returns:
            str: The subnet mask.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:ETHernet:MASK?"):
            return response.strip()
        raise ValueError("No subnet mask information returned.")

    # 1.4.31
    def setMASK(self, subnet_mask: str) -> None:
        """Set the subnet mask for the system's Ethernet functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:ETHernet:MASK <subnet_mask>

        Args:
            subnet_mask (str): The subnet mask to set.
        """
        if response := self.parent.cmd(
            f"SYSTem:COMMunicate:SOCKet:ETHernet:MASK {subnet_mask}"
        ):
            return response.strip()
        raise ValueError("No subnet mask information returned.")

    # 1.4.32
    def getGATEway(self) -> str:
        """Query the gateway for the system's Ethernet functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:ETHernet:GATEway?

        Returns:
            str: The gateway.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:ETHernet:GATEway?"):
            return response.strip()
        raise ValueError("No gateway information returned.")

    # 1.4.33
    def setGATEway(self, gateway: str) -> None:
        """Set the gateway for the system's Ethernet functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:ETHernet:GATEway <gateway>

        Args:
            gateway (str): The gateway to set.
        """
        if response := self.parent.cmd(
            f"SYSTem:COMMunicate:SOCKet:ETHernet:GATEway {gateway}"
        ):
            return response.strip()
        raise ValueError("No gateway information returned.")

    # 1.4.34
    def getMAC(self) -> str:
        """Query the MAC address for the system's Ethernet functionality.

        Command:
            SYSTem:COMMunicate:SOCKet:ETHernet:MAC?
        Returns:
            str: The MAC address.
        """
        if response := self.parent.cmd("SYSTem:COMMunicate:SOCKet:ETHernet:MAC?"):
            return response.strip()
        raise ValueError("No MAC address information returned.")

    # 1.4.35
    def initialize(self, enable: bool) -> None:
        """Initialize the Ethernet registry.

        Command:
            SYSTem:COMMunicate:SOCKet:ETHernet:INITialize

        Args:
            enable (bool): Set to True to initialize the Ethernet registry.
        """
        self.parent.cmd(f"SYSTem:COMMunicate:SOCKet:ETHernet:INITialize {int(enable)}")

    # 1.4.36
    def setKey(self, path: str, name: str, keyValue: str, valueType) -> None:
        """Write the key value to the registry.
        BINary is binary data, and each byte is
        separated by -, for example, binary data
        0x11, 0x22, 0xaa, 0xbb, expressed as "11-
        22-aa-bb";
        DWord is a 32-bit integer;
        ExpandString specifies a
        NULL-terminated string containing an
        unexpanded reference to an environment
        variable (such as %PATH%, which
        expands when the value is
        retrieved).MultiString is an array of strings,
        separating each string with -, and a single
        string needs to be enclosed in
        parentheses, for
        example"(abc)-(123er)-(hello,333)"
        QWord is a 64-bit integer
        String is a string

        Command: SYSTem:REGistry:DATA<QuoteStr>,<QuoteStr>,<QuoteStr>,BINary|DWord|ExpandString|MultiString|QWord|String

        Args:
            path (str): The path of the key: a quoted string
            name (str): The name of the key: a quoted string
            keyValue (str): The value of the key: a quoted string
            valueType (_type_): Value type
        """
        self.parent.cmd(f"SYSTem:REGistry:DATA{path},{name},{keyValue},{valueType}")

    # 1.4.37
    def getKey(self, path: str, name: str) -> str:
        """Read the key value from the registry.

        Command:
            SYSTem:REGistry:DATA? <QuoteStr>,<QuoteStr>

        Args:
            path (str): The path of the key.
            name (str): The name of the key.

        Returns:
            str: The value of the key.
        """
        if response := self.parent.cmd(f"SYSTem:REGistry:DATA? {path},{name}"):
            return response.strip()
        raise ValueError("No key value information returned.")

    # 1.4.38
    def deleteKey(self, path: str, name: str) -> None:
        """Delete the key from the registry.

        Command:
            SYSTem:REGistry:DELete<QuoteStr>,<QuoteStr>

        Args:
            path (str): The path of the key.
            name (str): The name of the key.
        """
        self.parent.cmd(f"SYSTem:REGistry:DELete {path},{name}")

    # 1.4.39
    def saveRegistry(self, keyName: str) -> None:
        """Save the registry to the file.

        Command:
            SYSTem:REGistry:SAVE HKEY_LOCAL_MACHINE|HKEY_CLASSES_ROOT|HKEY_CURRENT_USER|HKEY_USERS| ALL

        Args:
            keyName (str): The key name to save.
        """
        assert keyName in [
            "HKEY_LOCAL_MACHINE",
            "HKEY_CLASSES_ROOT",
            "HKEY_CURRENT_USER",
            "HKEY_USERS",
            "ALL",
        ]
        self.parent.cmd(f"SYSTem:REGistry:SAVE {keyName}")
