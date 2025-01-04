class DIFunctionChannelConfig(dict):
    """Data structure for channel configuration.

    channel_name (str): The name of the channel to configure.
    enabled (int): Enable or disable the channel (1 for enabled, 0 for disabled).
    label (str): A custom label for the channel.
    func_type (int): Function type, with the following values:
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
    range_index (int): The range index for the channel.
    delay (int): Channel delay.
    auto_range (int): Automatic range setting (1 for enabled, 0 for disabled).
    filters (int): Number of filters.
    other_params (str): Additional parameters based on the function type:
        - Voltage: High impedance or not.
        - Current: None.
        - Resistance: Wires, whether to open positive and negative current.
        - RTD/SPRT/Custom RTD: Sensor name, wires, sensor serial number, sensor ID,
        whether to open 1.4 times current, compensation interval.
        - Thermistor: Sensor name, wires, sensor serial number, sensor ID.
        - TC/Standard TC: Break detection, sensor name, sensor serial number,
        sensor ID, cold junction type (0 internal, 1 external, 2 custom),
        cold end fixed value, external cold junction channel name.
        - Switch: Switch type.
        - Current/Voltage Transmitter: Wires, sensor name, sensor serial number, sensor ID.

    Raises:
        ValueError: If the ElectricalFunctionType is not one of the expected values.
        TypeError: If the value of a key does not match the expected type.

    Returns:
        DIFunctionChannelConfig: An instance of DIFunctionChannelConfig.
    """

    valid_names = ['REF1', 'REF2', 'CH1-01A', 'CH1-01B', 'CH1-02A', 'CH1-02B', 'CH1-03A', 'CH1-03B', 'CH1-04A', 'CH1-04B', 'CH1-05A', 'CH1-05B', 'CH1-06A', 'CH1-06B', 'CH1-07A', 'CH1-07B', 'CH1-08A', 'CH1-08B', 'CH1-09A', 'CH1-09B', 'CH1-10A', 'CH1-10B']

    def validate_name(self, channel_name):
        assert channel_name in self.valid_names, f"Invalid channel name: {channel_name}"

    @classmethod
    def get_keys_and_types(self, **kwargs):
        types = {
            "Name": str,  # Channel name
            "Enabled": int,  # Enable or not
            "Label": str,  # Label
            "ElectricalFunctionType": int,  # Function type
            "Range": int,  # Range index
            "Delay": int,  # Channel delay
            "IsAutoRange": int,  # Automatic range or not
            "FilteringCount": int,  # Filter
        }

        func_type = kwargs.get("ElectricalFunctionType")

        function_handlers = {
            0: {"highImpedance": int},  # high impedence or not  # Voltage
            1: {},  # Current
            2: {  # Resistance
                "Wire": int,  # wires
                "IsOpenDetect": int,  # whether to open positive or negative current
            },
            3: {  # RTD
                "Wire": int,  # wires
                "SensorName": str,  # sensor name
                "SensorSN": str,  # sensor serial number
                "Id": str,  # sensor Id
                "IsSquareRooting2Current": int,  # whether to open 1.4 times current
                "CompensateInterval": int,  # compensation interval
            },
            4: {  # Thermistor
                "Wire": int,  # wires
                "SensorName": str,  # sensor name
                "SensorSN": str,  # sensor serial number
                "Id": str,  # sensor Id
            },
            100: {  # Thermocouple (TC)
                "IsOpenDetect": int,  # Whether the break detection
                "SensorName": str,  # sensor name
                "SensorSN": str,  # sensor serial number
                "Id": str,  # sensor Id
                "CjcType": int,  # cold junction type
                "CJCFixedValue": int,  # Was float, but we're trying int.,  # cold junction fixed value
                "CjcChannelName": str,  # custom cold junction channel name
            },
            101: {  # Switch
                # NOTE: Not specified in the documentation
            },
            102: {  # SPRT
                "Wire": int,  # wires
                "SensorName": str,  # sensor name
                "SensorSN": str,  # sensor serial number
                "Id": str,  # sensor Id
                "IsSquareRooting2Current": int,  # whether to open 1.4 times current
                "CompensateInterval": int,  # compensation interval
            },
            103: {"Wire": int, "SensorName": str, "SensorSN": str, "Id": str},  # Voltage Transmitter
            104: {"Wire": int, "SensorName": str, "SensorSN": str, "Id": str},  # Current Transmitter
            105: {  # Standard TC
                "IsOpenDetect": int,  # Whether the break detection
                "SensorName": str,  # sensor name
                "SensorSN": str,  # sensor serial number
                "Id": str,  # sensor Id
                "CjcType": int,  # cold junction type
                "CJCFixedValue": int,  # Was float, but we're trying int.,  # cold junction fixed value
                "CjcChannelName": str,  # custom cold junction channel name
            },
            106: {  # Custom RTD
                "Wire": int,  # wires
                "SensorName": str,  # sensor name
                "SensorSN": str,  # sensor serial number
                "Id": str,  # sensor Id
                "IsSquareRooting2Current": int,  # whether to open 1.4 times current
                "CompensateInterval": int,  # compensation interval
            },
            110: {  # Standard Resistance
                # NOTE: Not specified in the documentation
            },
        }

        if func_type in function_handlers:
            return {**types, **function_handlers[func_type]}
        raise ValueError(f"ElectricalFunctionType must be one of {list(function_handlers.keys())}, got {func_type}.")

    def __init__(self, **kwargs):
        for key, expected_type in self.get_keys_and_types(**kwargs).items():
            value = kwargs.get(key, None)
            self.validate(key, expected_type, value)
            self[key] = expected_type(value) if value is not None else ''
            self.validate_name(self.get('Name'))

    def validate(self, key, expected_type, value):
        if value is not None and not isinstance(value, expected_type):
            raise TypeError(f"Key '{key}' expects {expected_type}, got {type(value)}.")

    @classmethod
    def from_str(self, data: str):
        """Parse the channel configuration from a string."""
        if ';' in data:
            assert not data.split(';')[-1], "Trailing semicolon expected"
            return [self.from_str(d) for d in data.split(';')[:-1]]
        if not data:
            return None
        values = data.split(',')
        func_type = int(values[3])
        keys_and_types = self.get_keys_and_types(ElectricalFunctionType=func_type)
        keys = list(keys_and_types.keys())
        kwargs = {
            key: (keys_and_types[key](value) if value else None) for key, value in zip(keys, values)
        }
        assert len(kwargs) == len(keys), f"Missing keys: {keys}"
        assert str(self(**kwargs)) == data, f"Unexpected response: {data}\nExpected: {str(self(**kwargs))}"
        return self(**kwargs)

    def __str__(self):
        """Convert the DIFunctionChannelConfig object to a string representation."""
        keys = self.keys()
        return ','.join(str(self[key]) if self[key] is not None else '' for key in keys)
