# DIFunctionChannelConfig.py
class DIFunctionChannelConfig:
    """Class to represent a DI function channel configuration.

    Raises:
        ValueError: 
        TypeError: 
        ValueError: 
        TypeError: 

    Returns:
        DIFunctionChannelConfig: An instance of DIFunctionChannelConfig populated with the JSON data.
    """
    FUNCTION_HANDLERS = {
        0: {
                "highImpedance": int    # high impedence or not
            }, # Voltage
        1: {},  # Current
        2: {  # Resistance
                "Wire": int,            # wires
                "IsOpenDetect": bool,   # whether to open positive or negative current
            },
        3: {  # RTD
            "Wire": int,                        # wires
            "SensorName": str,                  # sensor name
            "SensorSN": str,                    # sensor serial number
            "Id": str,                          # sensor Id
            "IsSquareRooting2Current": bool,    # whether to open 1.4 times current
            "CompensateInterval": int,          # compensation interval
        },
        4: {  # Thermistor
            "Wire": int,  # wires
            "SensorName": str,  # sensor name
            "SensorSN": str,  # sensor serial number
            "Id": str,  # sensor Id
        },
        100: {  # Thermocouple (TC)
            "IsOpenDetect": bool,  # Whether the break detection
            "SensorName": str,  # sensor name
            "SensorSN": str,  # sensor serial number
            "Id": str,  # sensor Id
            "CjcType": int,  # cold junction type
            "CJCFixedValue": float,  # cold junction fixed value
            "CjcChannelName": str,  # custom cold junction channel name
        },
        101: {  # Switch
            # NOTE: Not specified in the documentation
        },
        102: {  # SPRT
            "Wire": int,  # wires
            "SensorName": str, # sensor name
            "SensorSN": str, # sensor serial number
            "Id": str, # sensor Id
            "IsSquareRooting2Current": bool, # whether to open 1.4 times current
            "CompensateInterval": int, # compensation interval
        },
        103: {"Wire": int, "SensorName": str, "SensorSN": str, "Id": str},  # Voltage Transmitter
        104: {"Wire": int, "SensorName": str, "SensorSN": str, "Id": str},  # Current Transmitter
        105: {  # Standard TC
            "IsOpenDetect": bool,  # Whether the break detection
            "SensorName": str,  # sensor name
            "SensorSN": str,  # sensor serial number
            "Id": str,  # sensor Id
            "CjcType": int,  # cold junction type
            "CJCFixedValue": float,  # cold junction fixed value
            "CjcChannelName": str,  # custom cold junction channel name
        },
        106: {  # Custom RTD
            "Wire": int,  # wires
            "SensorName": str, # sensor name
            "SensorSN": str, # sensor serial number
            "Id": str, # sensor Id
            "IsSquareRooting2Current": bool, # whether to open 1.4 times current
            "CompensateInterval": int, # compensation interval
        },
        110: {  # Standard Resistance
            # NOTE: Not specified in the documentation
        },
    }
    
    def get_keys_and_types(cls, **kwargs):
        types = {
            "Name": str,  # Channel name
            "Enabled": bool,  # Enable or not
            "Label": str,  # Label
            "ElectricalFunctionType": int,  # Function type
            "Range": int,  # Range index
            "Delay": int,  # Channel delay
            "IsAutoRange": bool,  # Automatic range or not
            "FilteringCount": int,  # Filter
        }

        func_type = kwargs.get("ElectricalFunctionType")

        if func_type not in cls.FUNCTION_HANDLERS:
            raise ValueError(f"Invalid ElectricalFunctionType: {func_type}")

        return {**types, **cls.FUNCTION_HANDLERS[func_type]}

    def __init__(cls, **kwargs):
        expected_types = cls.get_keys_and_types(**kwargs)
    
        for key, expected_type in expected_types.items():
            value = kwargs.get(key, None)
            if value is not None and not isinstance(value, expected_type):
                raise TypeError(f"Key '{key}' expects {expected_type}, got {type(value)}.")
            setattr(cls, key, value)
        cls.validateTypes()  # Validate the types of the attributes

    @classmethod
    def len(cls):
        return len([attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")])

    @classmethod
    def from_json(cls, data: dict):
        """Create a DIFunctionChannelConfig object from a JSON object.

        Parameters:
            data (dict): A dictionary containing the channel configuration.

        Returns:
            DIFunctionChannelConfig: An instance of DIFunctionChannelConfig populated with the JSON data.
        """
        keys_and_types = cls.get_keys_and_types(ElectricalFunctionType=data["ElectricalFunctionType"])
        keys = list(keys_and_types.keys())
        if not all(key in data for key in keys):
            raise KeyError(f"Missing keys in data: {keys}")

        kwargs = {key: (keys_and_types[key](data[key])) for key in keys}
        return cls(**kwargs)

    @classmethod
    def from_str(cls, data: str):
        """Parse the channel configuration from a string."""
        values = data.split(',')
        func_type = int(values[3])
        keys_and_types = cls.get_keys_and_types(ElectricalFunctionType=func_type)
        keys = list(keys_and_types.keys())
        kwargs = {key: (keys_and_types[key](value) if value else None) for key, value in zip(keys, values)}
        return cls(**kwargs)

    @classmethod
    def validateTypes(cls):
        keys_and_types = cls.get_keys_and_types(ElectricalFunctionType=cls.ElectricalFunctionType)
        for key, expected_type in keys_and_types.items():
            value = getattr(cls, key)
            if value is not None and not isinstance(value, expected_type):
                raise TypeError(f"Key '{key}' expects {expected_type}, got {type(value)}.")
