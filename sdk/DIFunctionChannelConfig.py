class DIFunctionChannelConfig:
    """Data structure for channel configuration.

    Raises:
        ValueError: If the ElectricalFunctionType is not one of the expected values.
        TypeError: If the value of a key does not match the expected type.

    Returns:
        DIFunctionChannelConfig: An instance of DIFunctionChannelConfig.
    """
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
        expected_types = self.get_keys_and_types(**kwargs)

        for key, expected_type in expected_types.items():
            value = kwargs.get(key, None)

            # Validate the type:
            if value is not None and not isinstance(value, expected_type):
                raise TypeError(f"Key '{key}' expects {expected_type}, got {type(value)}.")

            # Set the attribute:
            setattr(self, key, value)

    @classmethod
    def len(self):
        return len([
            attr
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("__")
        ])

    @classmethod
    def from_json(self, data: dict) -> "DIFunctionChannelConfig":
        """Create a DIFunctionChannelConfig object from a JSON object.


        Parameters:
            data (dict): A dictionary containing the channel configuration.


        Returns:
            DIFunctionChannelConfig: An instance of DIFunctionChannelConfig populated with the JSON data.
        """
        keys_and_types = self.get_keys_and_types(ElectricalFunctionType=data["ElectricalFunctionType"])
        keys = list(keys_and_types.keys())
        assert all(key in data for key in keys), f"Missing keys: {keys}"
        assert all(key in keys for key in data), f"Extra keys: {data.keys()}"
        kwargs = {key: (keys_and_types[key](data[key])) for key in keys}
        return self(**kwargs)

    @classmethod
    def from_str(self, data: str):
        """Parse the channel configuration from a string."""
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
        return self(**kwargs)

    def to_json(self):
        """Convert the DIFunctionChannelConfig object to a JSON-compatible dictionary."""
        result = {}
        for key in self.get_keys_and_types(ElectricalFunctionType=self.ElectricalFunctionType).keys():
            result[key] = getattr(self, key, None)
        return result

    def to_str(self):
        """Convert the DIFunctionChannelConfig object to a string representation."""
        keys = self.get_keys_and_types(ElectricalFunctionType=self.ElectricalFunctionType).keys()
        return ','.join('' if getattr(self, key) is None else str(getattr(self, key)) for key in keys)

    def __str__(self):
        """Convert the DIFunctionChannelConfig object to a string."""
        return self.to_str()

    def __repr__(self):
        """Represent the DIFunctionChannelConfig object as a string."""
        return self.to_json().__repr__()

    def __dict__(self):
        """Convert the DIFunctionChannelConfig object to a dictionary."""
        return self.to_json()
