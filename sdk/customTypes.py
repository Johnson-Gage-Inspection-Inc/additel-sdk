from typing import List, Optional

class type:
    class DIModuleInfo:
        """Data structure for module information.

        Identifier of box :The front
        panel is 0. The embedded
        junction box is 1. Then the
        seris-wound junction boxes
        are in 2, 3, 4

        Box type, 0=front panel,
        1=temperature box,
        2=process box
        Box hardware version
        Box software version
        Total number of box channel
        Label of box

        Each configuration includes:
            Index (int): Identifier of box (e.g., 0: front panel, 1: embedded junction box, 2-4: serial-wound junction boxes).
            Category (int): Module Category type.
            SN (str): Box serial number
            HwVersion (str): Hardware version of the module.
            SwVersion (str): Software version of the module.
            TotalChannelCount (int): Total number of channels in the module.
            Label (Optional[str]): Optional label for the module.
            ClassName (Optional[str]): Class name of the module (if provided).
        """
        def __init__(self,
                     Index: int,
                     Category: int,
                     SN: str,
                     HwVersion: str,
                     SwVersion: str,
                     TotalChannelCount: int,
                     Label: Optional[str] = None):
            self.Index = Index  # Identifier of the module
            self.Category = Category  # Box type (0: front panel, 1: temperature box, 2: process box)
            self.SN = SN  # Serial number of the module
            self.HwVersion = HwVersion  # Hardware version
            self.SwVersion = SwVersion  # Software version
            self.TotalChannelCount = TotalChannelCount  # Total number of channels
            self.Label = Label  # Optional label for the module

        @classmethod
        def from_json(cls, data: dict):
            """Create a DIModuleInfo object from a JSON object.

            Parameters:
                data (dict): A dictionary containing the module information.

            Returns:
                DIModuleInfo: An instance of DIModuleInfo populated with the JSON data.
            """
            if isinstance(data, dict):
                assert data['ClassName'] == 'DIModuleInfo', f"Class name mismatch: {data['ClassName']}"
                return cls(
                    Index=data['Index'],
                    Category=data['Category'],
                    SN=data['SN'],
                    HwVersion=data['HwVersion'],
                    SwVersion=data['SwVersion'],
                    TotalChannelCount=data['TotalChannelCount'],
                    Label=data['Label']
                )
            raise NotImplementedError(f"Invalid data type for DIModuleInfo.from_json: {type(data)}")

    class DIFunctionChannelConfig:
        """Data structure for function channel configuration.

            8+M values:
            First 8 (Always the same):
                1. Channel name.
                2. Enable or not
                3. Label
                4. Function type
                5. Range index
                6. Channel delay
                7. Automatic range or not
                8. Filter

            M additional parmeters (M depends on electrical logging type):
            voltage, M=1 (ElectricalFunctionType=0):
                1. high impedence or not;
            current, M=0 (ElectricalFunctionType=1):
                0. (None)
            resistances, M=2 (ElectricalFunctionType=2):
                1. wires,
                2. whether to open positive or negative current;
            RTD / SPRT/ custom RTD, M=6 (ElectricalFunctionType=3, 102, 106):
                1. wires,
                2. sensor name,
                3. sensor serial number,
                4. sensor Id,
                5. whether to open 1.4 times current,
                6. compensation interval;
            thermistors, M=4 (ElectricalFunctionType=4):
                1. wires,
                2. sensor name,
                3. sensor serial number,
                4. sensor Id;
            TC /standard TC. M=7 (ElectricalFunctionType=100, 105):
                1. Whether the break detection,
                2. sensor name,
                3. sensor serial number,
                4. sensor Id,
                5. cold junction type,
                6. cold junction fixed value,
                7. custom cold junction channel name;
            current / voltage transmitters, M=4 (ElectricalFunctionType=103, 104):
                + wires,
                + sensor name,
                + sensor serial number,
                + sensor Id;

        Each configuration includes:
            id (str): Unique identifier for the channel.
            name (str): The name of the channel to configure.
            enabled (bool): Enable or disable the channel (True for enabled, False for disabled).
            Label (Optional[str]): A custom Label for the channel.
            ElectricalFunctionType (int): Function type, with the following values:
                - 0: Voltage
                - 1: Current
                - 2: Resistance
                - 3: RTD
                - 4: Thermistor
                - 100: Thermocouple (TC)
                - 101: Switch
                - 102: SPRT
                - 103: Voltage Transmitter
                - 104: Current Transmitter
                - 105: Standard TC
                - 106: Custom RTD
                - 110: Standard Resistance
            range_Index (int): The range Index for the channel.
            delay (int): Channel delay.
            auto_range (bool): Automatic range setting (True for enabled, False for disabled).
            filters (int): Number of filters.
            wire (Optional[int]): Number of wires for the configuration (e.g., 2, 3, or 4).
            sensor_name (Optional[str]): Name of the sensor.
            sensor_sn (Optional[str]): Serial number of the sensor.
            CompensateInterval (Optional[int]): Compensation interval for the sensor.
            IsSquareRooting2Current (Optional[bool]): Whether square rooting is applied.
            IsCurrentCommutation (Optional[bool]): Whether current commutation is enabled.
        """
        def __init__(self, Name: str, Enabled: bool, Label: str, ElectricalFunctionType: int, Range: int, Delay: int, IsAutoRange: bool, FilteringCount: int,
                     Wire: int = None, CompensateInterval: int = None, IsSquareRooting2Current: bool = None, IsCurrentCommutation: bool = None, SensorName: str = None,
                     SensorSN: str = None, Id: str = None, ChannelInfo1: str = None, ChannelInfo2: str = None, ChannelInfo3: str = None, ClassName: str = None,
                     highImpedance: int = None, IsOpenDetect: bool = None, CjcType: int = None, CJCFixedValue: float = None,
                    CjcChannelName: str = None):
            """Initialize the DIFunctionChannelConfig object.

            Args:
                Wire (int):
                CompensateInterval (int):
                IsSquareRooting2Current (bool):
                IsCurrentCommutation (bool):
                SensorName (str):
                SensorSN (str):
                Id (str): Unique identifier for the channel
                Name (str): Channel name
                Enabled (bool):
                Label (str):
                ElectricalFunctionType (int):
                IsAutoRange (bool):
                Range (int):
                Delay (int):
                FilteringCount (int):
                ChannelInfo1 (str):
                ChannelInfo2 (str):
                ChannelInfo3 (str):
                ClassName (str): DIFunctionChannelConfig
            """
            self.Name = Name
            self.Enabled = Enabled
            self.Label = Label
            self.ElectricalFunctionType = ElectricalFunctionType
            self.Range = Range
            self.Delay = Delay
            self.IsAutoRange = IsAutoRange
            self.FilteringCount = FilteringCount

            # M additional parmeters (M depends on electrical logging type):
            if ElectricalFunctionType == 0:
                M = 1
                self.highImpedance = highImpedance
                raise NotImplementedError("Voltage function not implemented")

            elif ElectricalFunctionType == 1:
                M = 0
                raise NotImplementedError("Current function not implemented")

            if ElectricalFunctionType in [2, 3, 4, 102, 103, 104, 106]:
                self.Wire = Wire
                if ElectricalFunctionType == 2:
                    M = 2
                    raise NotImplementedError("Resistance function not implemented")

                self.SensorName = SensorName
                self.SensorSN = SensorSN
                self.Id = Id
                if ElectricalFunctionType in [4, 103, 104]:
                    M = 4
                    raise NotImplementedError("Thermistor and Current/Voltage Transmitter functions not implemented")
                else:
                    M = 6
                    self.IsSquareRooting2Current = IsSquareRooting2Current
                    self.CompensateInterval = CompensateInterval

            elif ElectricalFunctionType in [100, 105]:
                M = 7
                self.IsOpenDetect = IsOpenDetect
                self.SensorName = SensorName
                self.SensorSN = SensorSN
                self.Id = Id
                self.CjcType = CjcType
                self.CJCFixedValue = CJCFixedValue
                self.CjcChannelName = CjcChannelName

            else:
                raise ValueError(f"Invalid ElectricalFunctionType: {ElectricalFunctionType}")

            self.validateLength(self.len(), M=M)

            # self.Wire = Wire
            # self.CompensateInterval = CompensateInterval
            # self.IsSquareRooting2Current = IsSquareRooting2Current
            # self.IsCurrentCommutation = IsCurrentCommutation
            # self.SensorName = SensorName
            # self.SensorSN = SensorSN
            # self.Id = Id
            # self.ChannelInfo1 = ChannelInfo1
            # self.ChannelInfo2 = ChannelInfo2
            # self.ChannelInfo3 = ChannelInfo3
            # self.ClassName = ClassName

        @classmethod
        def len(self):
            # Count the number of parameters
            return len([attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")])

        @classmethod
        def from_json(cls, data: dict):
            """Create a DIFunctionChannelConfig object from a JSON object.

            Parameters:
                data (dict): A dictionary containing the channel configuration.

            Returns:
                DIFunctionChannelConfig: An instance of DIFunctionChannelConfig populated with the JSON data.
            """
            if isinstance(data, dict):
                return cls(
                    Name=data['Name'],
                    Enabled=data['Enabled'],
                    Label=data['Label'],
                    ElectricalFunctionType=data['ElectricalFunctionType'],
                    Range=data['Range'],
                    Delay=data['Delay'],
                    IsAutoRange=data['IsAutoRange'],
                    FilteringCount=data['FilteringCount'],
                    Wire=data.get('Wire', 0),
                    CompensateInterval=data.get('CompensateInterval', 0),
                    IsSquareRooting2Current=data.get('IsSquareRooting2Current', False),
                    IsCurrentCommutation=data.get('IsCurrentCommutation', False),
                    SensorName=data.get('SensorName', ''),
                    SensorSN=data.get('SensorSN', ''),
                    Id=data.get('Id', ''),
                    ChannelInfo1=data.get('ChannelInfo1', ''),
                    ChannelInfo2=data.get('ChannelInfo2', ''),
                    ChannelInfo3=data.get('ChannelInfo3', ''),
                    ClassName=data.get('ClassName', '')
                )
            raise NotImplementedError(f"Invalid data type for DIFunctionChannelConfig.from_json: {type(data)}")

        @classmethod
        def from_str(cls, data: str):
            """Create a DIFunctionChannelConfig object from a string.

            Parameters:
                data (str): A string containing the channel configuration.

            Returns:
                DIFunctionChannelConfig: An instance of DIFunctionChannelConfig populated with the string data.
            """
            if isinstance(data, str):
                # Split the string into a list of values
                values = data.split(',')
                # Check if the list contains the expected number of values
                if len(values) >= 8:
                    # Extract the values from the list
                    funcType = int(values[3])

                    # Required variables:
                    payload = {
                        "Name": values[0],                          # 1. Channel name.
                        "Enabled": bool(int(values[1])),            # 2. Enable or not
                        "Label": values[2],                         # 3. Label
                        "ElectricalFunctionType": funcType,         # 4. Function type
                        "Range": int(values[4]),                    # 5. Range index
                        "Delay": int(values[5]),                    # 6. Channel delay
                        "IsAutoRange": bool(int(values[6])),        # 7. Automatic range or not
                        "FilteringCount": int(values[7])            # 8. Filter
                    }

                    # M additional parmeters (M depends on electrical logging type):
                    if funcType == 0:
                        M = 1
                        payload['highImpedance'] = int(values[8])
                        raise NotImplementedError("Voltage function not implemented")

                    elif funcType == 1:
                        M = 0
                        cls.validateLength(values, M=0)
                        raise NotImplementedError("Current function not implemented")

                    elif funcType == 2:
                        M = 2
                        payload['Wire'] = values[8]
                        raise NotImplementedError("Resistance function not implemented")

                    elif funcType in [3, 102, 106]:
                        M = 6
                        payload['Wire'] = values[8]
                        payload['SensorName'] = values[9]
                        payload['SensorSN'] = values[10]
                        payload['Id'] = values[11]
                        payload['IsSquareRooting2Current'] = bool(int(values[12]))
                        payload['CompensateInterval'] = int(values[13])
                        pass

                    elif funcType in [100, 105]:
                        M = 7
                        payload['IsOpenDetect'] = bool(int(values[8]))
                        payload['SensorName'] = values[9]
                        payload['SensorSN'] = values[10]
                        payload['Id'] = values[11]
                        payload['CjcType'] = int(values[12])
                        payload['CJCFixedValue'] = float(values[13])
                        payload['CjcChannelName'] = values[14]

                    elif funcType in [4, 103, 104]:
                        M = 4
                        payload['Wire'] = values[8]
                        payload['SensorName'] = values[9]
                        payload['SensorSN'] = values[10]
                        payload['id'] = values[11]
                        raise NotImplementedError("Thermistor and Current/Voltage Transmitter functions not implemented")

                    else:
                        raise ValueError(f"Invalid ElectricalFunctionType: {funcType}")

                    cls.validateLength(values, M=M)
                    return cls(**payload)
                raise ValueError(f"Invalid number of values for DIFunctionChannelConfig: {len(values)}")
            raise NotImplementedError(f"Invalid data type for DIFunctionChannelConfig.from_str: {type(data)}")

        @classmethod
        def validateLength(cls, values, M):
            if isinstance(values, list):
                assert len(values) == (8 + M), f"Invalid number of values for Current: {len(values)}"
            elif isinstance(values, cls):
                assert values.len() == (8 + M), f"Invalid number of values for Current: {values.len()}"

    class DIScanInfo:
        """Data structure for scanning information.

        Each configuration includes:
            nplc (int): Number of Power Line Cycles (NPLC).
            sampling_frequency (int): Sampling frequency cycle.
            channels (List[str]): List of channels being scanned.
        """
        def __init__(self,
                    nplc: int,
                    sampling_frequency: int,
                    channels: List[str]):
            self.nplc = nplc  # Number of Power Line Cycles (NPLC)
            self.sampling_frequency = sampling_frequency  # Sampling frequency cycle
            self.channels = channels  # List of channels being scanned
