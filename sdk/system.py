from typing import Optional

# Section 1.4 - System Commands

class System:
    def __init__(self, parent):
        self.parent = parent
        self.communicate = self.Communicate(self)

    # 1.4.1
    def getVersion(self, module: Optional[str] = None) -> dict:
        """
        Retrieve version information for the system or a specific module.

        Command:
            SYSTem:VERSion? [<module>]

        Parameters:
            module (str, optional): The module for which to retrieve version information.
                Valid options include "APPLication", "ElECtricity:FIRMware", "ElECtricity:HARDware",
                "OS:FIRMware", "OS:HARDware", "JUNCtion:HARDware", "JUNCtion:FIRMware".
                If not provided, retrieves general SCIP version information.

        Returns:
            dict: A dictionary containing version information.

        Example:
            {"SCIP": "v1.0", "Application": "v1.2"}
        """
        command = f'SYSTem:VERSion? {module}' if module else 'SYSTem:VERSion?'
        response = self.parent.send_command(command)
        if response:
            return {key_value.split(":")[0]: key_value.split(":")[1] for key_value in response.split(",")}
        return {}

    # 1.4.2
    def get_next_error(self) -> dict:
        """
        Retrieve the next error in the system error queue.

        Command:
            SYSTem:ERRor[:NEXT]?

        Returns:
            dict: A dictionary containing:
                - "error_code" (int): The error code from the system.
                - "error_message" (str): A description of the error.

        Raises:
            ValueError: If no error information is returned.
        """
        response = self.parent.send_command("SYSTem:ERRor:NEXT?")
        if response:
            parts = response.split(",")
            return {
                "error_code": int(parts[0]),
                "error_message": parts[1].strip()
            }
        raise ValueError("No error information returned.")

    # 1.4.3
    def set_date(self, year: int, month: int, day: int):
        """
        Set the system date.

        Command:
            SYSTem:DATE <year>,<month>,<day>

        Parameters:
            year (int): Year to set.
            month (int): Month to set (1-12).
            day (int): Day to set (1-31).

        Returns:
            None
        """
        command = f"SYSTem:DATE {year},{month},{day}"
        self.parent.send_command(command)

    # 1.4.4
    def get_date(self) -> dict:
        """
        Query the system date.

        Command:
            SYSTem:DATE?

        Parameters:
            None

        Returns:
            dict: A dictionary containing:
                - "year" (int): Current year.
                - "month" (int): Current month.
                - "day" (int): Current day.
        """
        response = self.parent.send_command("SYSTem:DATE?")
        if response:
            parts = response.split(",")
            return {
                "year": int(parts[0]),
                "month": int(parts[1]),
                "day": int(parts[2])
            }
        raise ValueError("No date information returned.")

    # 1.4.5
    def set_time(self, hour: int, minute: int, second: int):
        """
        Set the system time.

        Command:
            SYSTem:TIME <hour>,<minute>,<second>

        Parameters:
            hour (int): Hour to set (0-23).
            minute (int): Minute to set (0-59).
            second (int): Second to set (0-59).

        Returns:
            None
        """
        command = f"SYSTem:TIME {hour},{minute},{second}"
        self.parent.send_command(command)

    # 1.4.6
    def set_local_lock(self, lock: bool):
        """
        Set the local lock-out state of the system.

        Command:
            SYSTem:KLOCk <Boolean>|ON|OFF

        Parameters:
            lock (bool): Set to True to lock the system (ON) or False to unlock it (OFF).

        Returns:
            None
        """
        command = f"SYSTem:KLOCk {int(lock)}"
        self.parent.send_command(command)

    # 1.4.7
    def get_local_lock(self) -> bool:
        """
        Query the local lock-out state of the system.

        Command:
            SYSTem:KLOCk?

        Parameters:
            None

        Returns:
            bool: True if the system is locked (ON), False if unlocked (OFF).
        """
        response = self.parent.send_command("SYSTem:KLOCk?")
        if response:
            return bool(response.strip())
        raise ValueError("No lock state information returned.")
    
    # 1.4.8
    def set_warning_tone(self, enable: bool):
        """
        Set the state of the system's warning tone.

        Command:
            SYSTem:BEEPer:ALARm <Boolean>|ON|OFF

        Parameters:
            enable (bool): Set to True to enable the warning tone (ON) or False to disable it (OFF).

        Returns:
            None
        """
        command = f"SYSTem:BEEPer:ALARm {int(enable)}"
        self.parent.send_command(command)

    # 1.4.9
    def set_keypad_tone(self, enable: bool):
        """
        Set the state of the keypad tone.

        Command:
            SYSTem:BEEPer:TOUCh <Boolean>|ON|OFF

        Parameters:
            enable (bool): Set to True to enable the keypad tone (ON) or False to disable it (OFF).

        Returns:
            None
        """
        command = f"SYSTem:BEEPer:TOUCh {int(enable)}"
        self.parent.send_command(command)

    class Password():
        def __init__(self, parent):
            self.parent = parent

        # 1.4.40
        def setPassword(self, old_password: str, new_password: str, new_password_confirm: str):
            """
            Edit the user password

            Command:
                SYSTem:PASSword <password>

            Parameters:
                old_password (str): The old password.
                new_password (str): The new password.
                new_password_confirm (str): The new password confirmation.

            Returns:
                None
            """
            self.parent.send_command(f"SYSTem:PASSword {old_password},{new_password},{new_password_confirm}")

        # 1.4.41
        def getProtection(self) -> bool:
            """
            Query that the protection of sensor bank
            password is opened or not

            Command:
                SYSTem:PASSword:ENABle:SENSor?
            
            Parameters:
                None

            Returns:
                bool: True if the protection of sensor bank password is opened, False if not.
            """
            if response := self.parent.send_command("SYSTem:PASSword:ENABle:SENSor?"):
                return bool(response.strip())
            raise ValueError("No protection information returned.")
        
        # 1.4.42
        def setProtection(self, enable: bool):
            """
            Set the protection of sensor bank password

            Command:
                SYSTem:PASSword:ENABle:SENSor <enable>

            Parameters:
                enable (bool): Set to True to enable the protection of sensor bank password.

            Returns:
                None
            """
            self.parent.send_command(f"SYSTem:PASSword:ENABle:SENSor {int(enable)}")

    class Communicate:
        def __init__(self, parent):
            self.parent = parent
            self.WLAN = self.WLAN(self)
            self.Ethernet = self.Ethernet(self)
            self.Bluetooth = self.Bluetooth(self)

        class WLAN:
            def __init__(self, parent):
                self.parent = parent

            # 1.4.10
            def setstate(self, enable: bool):
                """
                Set the state of the system's WiFi functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:WLAN[:STATe] <Boolean>|ON|OFF

                Parameters:
                    enable (bool): Set to True to enable WiFi (ON) or False to disable it (OFF).

                Returns:
                    None
                """
                command = f"SYSTem:COMMunicate:SOCKet:WLAN:STATe {int(enable)}"
                self.parent.send_command(command)

            # 1.4.11
            def getstate(self) -> bool:
                """
                Query the state of the system's WiFi functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:WLAN[:STATe]?

                Parameters:
                    None

                Returns:
                    bool: True if WiFi is enabled (ON), False if disabled (OFF).
                """
                response = self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:STATe?")
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

                Parameters:
                    ip_address (str): The IP address to set.

                Returns:
                    None
                """
                # FIXME: Validate IP address format
                command = f"SYSTem:COMMunicate:SOCKet:WLAN:ADDRess {ip_address}"
                self.parent.send_command(command)

            # 1.4.13
            def get_ip_address(self) -> str:
                """
                Query the IP address for the system's WiFi functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:WLAN:ADDRess?

                Parameters:
                    None

                Returns:
                    str: The IP address.
                """
                if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:ADDRess?"):
                    return response.strip()
                raise ValueError("No IP address information returned.")
            
            # 1.4.14
            def set_subnet_mask(self, subnet_mask: str):
                """
                Set the subnet mask for the system's WiFi functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:WLAN:MASK <subnet_mask>

                Parameters:
                    subnet_mask (str): The subnet mask to set.

                Returns:
                    None
                """
                if response := self.parent.send_command(f"SYSTem:COMMunicate:SOCKet:WLAN:MASK {subnet_mask}"):
                    return response.strip()
                raise ValueError("No subnet mask information returned.")

            # 1.4.15
            def get_subnet_mask(self) -> str:
                """
                Query the subnet mask for the system's WiFi functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:WLAN:MASK?

                Parameters:
                    None

                Returns:
                    str: The subnet mask.
                """
                if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:MASK?"):
                    return response.strip()
                raise ValueError("No subnet mask information returned.")
            
            # 1.4.16
            def setGateway(self, IPaddress: str):
                """
                Set the gateway for the system's WiFi functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:WLAN:GATEway <gateway>

                Parameters:
                    IPaddress (str): The gateway to set.

                Returns:
                    None
                """
                if response := self.parent.send_command(f"SYSTem:COMMunicate:SOCKet:WLAN:GATEway {IPaddress}"):
                    return response.strip()
                raise ValueError("No gateway information returned.")
            
            # 1.4.17
            def getGateway(self) -> str:
                """
                Query the gateway for the system's WiFi functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:WLAN:GATEway?

                Parameters:
                    None

                Returns:
                    str: The gateway.
                """
                if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:GATEway?"):
                    return response.strip()
                raise ValueError("No gateway information returned.")
            
            # 1.4.18
            def getMAC(self) -> str:
                """
                Query the MAC address for the system's WiFi functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:WLAN:MAC?

                Parameters:
                    None

                Returns:
                    str: The MAC address.
                """
                if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:MAC?"):
                    return response.strip()
                raise ValueError("No MAC address information returned.")
            
            # 1.4.19
            def setDHCP(self, enable: bool):
                """
                Set the DHCP state for the system's WiFi functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:WLAN:DHCP <Boolean>|ON|OFF

                Parameters:
                    enable (bool): Set to True to enable DHCP (ON) or False to disable it (OFF).

                Returns:
                    None
                """
                command = f"SYSTem:COMMunicate:SOCKet:WLAN:DHCP {int(enable)}"
                self.parent.send_command(command)

            # 1.4.20
            def getDHCP(self) -> bool:
                """
                Query the DHCP state for the system's WiFi functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:WLAN:DHCP?

                Parameters:
                    None

                Returns:
                    bool: True if DHCP is open (1), False if closed (0).
                """
                response = self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:DHCP?")
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

                Parameters:
                    ssid (str): The SSID to set.

                Returns:
                    {[“ssid: way of encryption”]}
                """
                if response := self.parent.send_command(f"SYSTem:COMMunicate:SOCKet:WLAN:SSID {ssid}"):
                    return response.strip()
                raise ValueError("No SSID information returned.")
            
            # 1.4.22
            def connect(self, ssid: str, password: str):
                """
                Connect to a WiFi network.

                Command:
                    SYSTem:COMMunicate:SOCKet:WLAN:CONNect <ssid>,<password>

                Parameters:
                    ssid (str): hot spot name, the character string with quotation
                    encryptionMode, WEP_OFF, WEP_ON, WEP_AUTO, WPA_PSK, WPA_TKIP, WPA2_PSK, WPA2_AES,CCKM_TKIP, WEP_CKIP, WEP_AUTO_CKIP, CCKM_AES, WPA_PSK_AES, WPA_AES, WPA2_PSK_TKIP, WPA2_TKIP, WAPI_PSK, WAPI_CERT
                    password (str): The password for the WiFi network, the character string with quotation

                Returns:
                    None
                """
                command = f"SYSTem:COMMunicate:SOCKet:WLAN:CONNect {ssid},{password}"
                self.parent.send_command(command)

            # 1.4.23
            def getConnection(self) -> str:
                """
                Query the connection status of the system's WiFi functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:WLAN:CONNect?

                Parameters:
                    None

                Returns:
                    str: The connection status.
                """
                if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:CONNect?"):
                    return response.strip()
                raise ValueError("No connection information returned.")
            
            # 1.4.24
            def disconnect(self):
                """
                Disconnect from the current WiFi network.

                Command:
                    SYSTem:COMMunicate:SOCKet:WLAN:DISConnect

                Parameters:
                    None

                Returns:
                    None
                """
                self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:DISConnect")

            # 1.4.25
            def getDBM(self):
                """Query signal strength and dBm value of WIFI

                Command:
                    SYSTem:COMMunicate:SOCKet:WLAN:DBM?

                Parameters:
                    None

                Returns:
                    str: The signal strength and dBm value.
                """
                if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:WLAN:DBM?"):
                    return response.strip()
                raise ValueError("No signal strength information returned.")
            
        class Ethernet:
            def __init__(self, parent):
                self.parent = parent

            # 1.4.26
            def getDHCP(self) -> bool:
                """
                Query the DHCP state for the system's Ethernet functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:ETHernet:DHCP?

                Parameters:
                    None

                Returns:
                    bool: True if DHCP is open (1), False if closed (0).
                """
                response = self.parent.send_command("SYSTem:COMMunicate:SOCKet:ETHernet:DHCP?")
                if response:
                    return bool(response.strip())
                raise ValueError("No DHCP state information returned.")
            
            # 1.4.27
            def setDHCP(self, enable: bool):
                """
                Set the DHCP state for the system's Ethernet functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:ETHernet:DHCP <Boolean>|ON|OFF

                Parameters:
                    enable (bool): Set to True to enable DHCP (ON) or False to disable it (OFF).

                Returns:
                    None
                """
                command = f"SYSTem:COMMunicate:SOCKet:ETHernet:DHCP {int(enable)}"
                self.parent.send_command(command)

            # 1.4.28
            def getIP(self) -> str:
                """
                Query the IP address for the system's Ethernet functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:ETHernet:ADDRess?

                Parameters:
                    None

                Returns:
                    str: The IP address.
                """
                if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:ETHernet:ADDRess?"):
                    return response.strip()
                raise ValueError("No IP address information returned.")
            
            # 1.4.29
            def setIP(self, ip_address: str):
                """
                Set the IP address for the system's Ethernet functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:ETHernet:ADDRess <ip_address>

                Parameters:
                    ip_address (str): The IP address to set.

                Returns:
                    None
                """
                if response := self.parent.send_command(f"SYSTem:COMMunicate:SOCKet:ETHernet:ADDRess {ip_address}"):
                    return response.strip()
                raise ValueError("No IP address information returned.")
            
            # 1.4.30
            def getMASK(self) -> str:
                """
                Query the subnet mask for the system's Ethernet functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:ETHernet:MASK?

                Parameters:
                    None

                Returns:
                    str: The subnet mask.
                """
                if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:ETHernet:MASK?"):
                    return response.strip()
                raise ValueError("No subnet mask information returned.")
            
            # 1.4.31
            def setMASK(self, subnet_mask: str):
                """
                Set the subnet mask for the system's Ethernet functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:ETHernet:MASK <subnet_mask>

                Parameters:
                    subnet_mask (str): The subnet mask to set.

                Returns:
                    None
                """
                if response := self.parent.send_command(f"SYSTem:COMMunicate:SOCKet:ETHernet:MASK {subnet_mask}"):
                    return response.strip()
                raise ValueError("No subnet mask information returned.")
            
            # 1.4.32
            def getGATEway(self) -> str:
                """
                Query the gateway for the system's Ethernet functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:ETHernet:GATEway?

                Parameters:
                    None

                Returns:
                    str: The gateway.
                """
                if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:ETHernet:GATEway?"):
                    return response.strip()
                raise ValueError("No gateway information returned.")
            
            # 1.4.33
            def setGATEway(self, gateway: str):
                """
                Set the gateway for the system's Ethernet functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:ETHernet:GATEway <gateway>

                Parameters:
                    gateway (str): The gateway to set.

                Returns:
                    None
                """
                if response := self.parent.send_command(f"SYSTem:COMMunicate:SOCKet:ETHernet:GATEway {gateway}"):
                    return response.strip()
                raise ValueError("No gateway information returned.")
            
            # 1.4.34
            def getMAC(self) -> str:
                """
                Query the MAC address for the system's Ethernet functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:ETHernet:MAC?

                Parameters:
                    None

                Returns:
                    str: The MAC address.
                """
                if response := self.parent.send_command("SYSTem:COMMunicate:SOCKet:ETHernet:MAC?"):
                    return response.strip()
                raise ValueError("No MAC address information returned.")
            
            # 1.4.35
            def initialize(self, enable: bool):
                """
                Initialize the Ethernet registry.

                Command:
                    SYSTem:COMMunicate:SOCKet:ETHernet:INITialize

                Parameters:
                    enable (bool): Set to True to initialize the Ethernet registry.

                Returns:
                    None
                """
                self.parent.send_command(f"SYSTem:COMMunicate:SOCKet:ETHernet:INITialize {int(enable)}")

            # 1.4.36
            def setKey(self, path: str, name: str, keyValue: str, valueType):
                """
                Write the key value to the registry.
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

                Returns:
                    None
                """
                self.parent.send_command(f"SYSTem:REGistry:DATA{path},{name},{keyValue},{valueType}")

            # 1.4.37
            def getKey(self, path: str, name: str) -> str:
                """
                Read the key value from the registry.

                Command:
                    SYSTem:REGistry:DATA? <QuoteStr>,<QuoteStr>

                Parameters:
                    path (str): The path of the key.
                    name (str): The name of the key.

                Returns:
                    str: The value of the key.
                """
                if response := self.parent.send_command(f"SYSTem:REGistry:DATA? {path},{name}"):
                    return response.strip()
                raise ValueError("No key value information returned.")
            
            # 1.4.38
            def deleteKey(self, path: str, name: str):
                """
                Delete the key from the registry.

                Command:
                    SYSTem:REGistry:DELete<QuoteStr>,<QuoteStr>

                Parameters:
                    path (str): The path of the key.
                    name (str): The name of the key.

                Returns:
                    None
                """
                self.parent.send_command(f"SYSTem:REGistry:DELete {path},{name}")

            # 1.4.39
            def saveRegistry(self, keyName: str):
                """
                Save the registry to the file.

                Command:
                    SYSTem:REGistry:SAVE HKEY_LOCAL_MACHINE|HKEY_CLASSES_ROOT|HKEY_CURRENT_USER|HKEY_USERS| ALL

                Parameters:
                    keyName (str): The key name to save.
                
                Returns:
                    None
                """
                assert(keyName in ["HKEY_LOCAL_MACHINE", "HKEY_CLASSES_ROOT", "HKEY_CURRENT_USER", "HKEY_USERS", "ALL"])
                self.parent.send_command(f"SYSTem:REGistry:SAVE {keyName}")

        class Bluetooth:
            def __init__(self, parent):
                self.parent = parent

            # 1.4.43
            def setstate(self, enable: bool):
                """
                Set the state of the system's Bluetooth functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:BLUetooth[:STATe] <Boolean>|ON|OFF

                Parameters:
                    enable (bool): Set to True to enable Bluetooth (ON) or False to disable it (OFF).

                Returns:
                    None
                """
                command = f"SYSTem:COMMunicate:SOCKet:BLUetooth:STATe {int(enable)}"
                self.parent.send_command(command)

            # 1.4.44
            def getstate(self) -> bool:
                """
                Query the state of the system's Bluetooth functionality.

                Command:
                    SYSTem:COMMunicate:SOCKet:BLUetooth[:STATe]?

                Parameters:
                    None

                Returns:
                    bool: True if Bluetooth is enabled (ON), False if disabled (OFF).
                """
                response = self.parent.send_command("SYSTem:COMMunicate:SOCKet:BLUetooth:STATe?")
                if response:
                    return bool(response.strip())
                raise ValueError("No Bluetooth state information returned.")
            
            # 1.4.45
            def getName(self) -> str:
                """
                Query the name of the Bluetooth device.

                Command:
                    SYSTem:COMMunicate:BLUEtooth:NAMe?

                Parameters:
                    None

                Returns:
                    str: The name of the Bluetooth device.
                """
                if response := self.parent.send_command("SYSTem:COMMunicate:BLUEtooth:NAMe?"):
                    return response.strip()
                raise ValueError("No Bluetooth name information returned.")
                
            # 1.4.46 (SYSTem:COMMunicate:BLUEtooth:NAMe<UnquoStr>))
            def setName(self, name: str):
                """
                Set the name of the Bluetooth device.

                Command:
                    SYSTem:COMMunicate:BLUEtooth:NAMe <UnquoStr>

                Parameters:
                    name (str): The name to set.

                Returns:
                    None
                """
                self.parent.send_command(f"SYSTem:COMMunicate:BLUEtooth:NAMe {name}")
