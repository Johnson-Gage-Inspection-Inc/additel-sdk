from datetime import datetime
from typing import List, Union
import re
import logging

def coerce(adt: Union[dict, str, list], map: dict = None):
    """
    Dynamically coerces a dictionary-based object to its appropriate type
    using a provided type mapping.

    Args:
        adt (dict or str): The dictionary containing the Additel-formatted data to coerce.
        map (dict): A mapping of type strings to Python types/classes.
        date_format (str): Optional format string for parsing datetime objects.

    Returns:
        An instance of the type determined from the `$type` key in the dictionary.

    Raises:
        TypeError: If `$type` is missing or not recognized in the provided map.
    """

    def coerce_list(adt: list, map: dict):
        return [coerce(v, map) if isinstance(v, dict) else v for v in adt]

    if isinstance(adt, list):
        return coerce_list(adt, map)

    adt = json(adt)  # Ensure it's a dictionary

    if not map:
        map = load_mapping()

    if typeStr := adt.pop('$type', None):
        ClassName = adt.pop('ClassName', None)  # noqa: F841
        listIndicator = r'System\.Collections\.Generic\.List`1\[\[([\w\.]+), ([\w\.]+)\]\], ([\w\.]+)'
        if match := re.match(listIndicator, typeStr):
            typ = List[map[match.group(1)]]
            adt = adt['$values']
            return coerce_list(adt, map)
        else:
            typeStr, _ = typeStr.split(',')
            typ = map[typeStr]

        if typeStr not in map:
            raise TypeError(f"Unknown type: {typeStr}. Full map: {map}")

        # Handle date formatting
        if typ == datetime:
            return datetime.strptime(adt['TickTime'], '%Y-%m-%d %H:%M:%S %f')

        # Recursively coerce nested dictionaries:
        for key, value in adt.items():
            if isinstance(value, dict):
                adt[key] = coerce(value, map)
            elif isinstance(value, list):
                adt[key] = [coerce(v, map) for v in value]

        return typ(**adt)    # Instantiate the type with the coerced dictionary

    # If you made it this far, the dictionary was already coerced
    # Prevent an infinite loop by returning the dictionary if no type is specified
    return adt  # Return the already coerced dictionary

def json(obj) -> dict:
    """Coerce an object to a dictionary.

    Args:
        obj: A dictionary or JSON string.

    Returns:
        dict: The dictionary representation of the object.
    """
    if isinstance(obj, str):
        from json import loads
        try:
            obj = loads(obj)
        except ValueError:
            logging.warning(f"Failed to parse JSON string: {obj}")
            return obj
    if isinstance(obj, dict):
        return obj
    raise NotImplementedError(f"Unsupported type for dictionary coercion: {type(obj)}")

def load_mapping():
    from .scan import DIScanInfo, DIReading
    from .module import DIModuleInfo
    from .channel import DIFunctionChannelConfig
    map = {
        'System.Double': float,
        # - 0: Voltage
        # - 1: Current
        # - 2: Resistance
        'TAU.Module.Channels.DI.DIFunctionRTDChannelConfig': DIFunctionChannelConfig,
        # - 4: Thermistor
        # - 100: Thermocouple (TC)
        # - 101: Switch
        'TAU.Module.Channels.DI.DIFunctionSPRTChannelConfig': DIFunctionChannelConfig,  # NOTE: This is a guess
        # - 103: Voltage Transmitter
        # - 104: Current Transmitter
        # - 105: Standard TC
        # - 106: Custom RTD
        # - 110: Standard Resistance
        'TAU.Module.Channels.DI.DIFunctionChannelConfig': DIFunctionChannelConfig,
        'TAU.Module.Channels.DI.DIScanInfo': DIScanInfo,
        'TAU.Module.Channels.DI.DIModuleInfo': DIModuleInfo,
        'TAU.Module.Channels.DI.DIReading': DIReading,
        'TAU.Module.Channels.DI.DITemperatureReading': DIReading,
        'TAU.Module.Channels.DI.DIElectricalReading': DIReading,
        'TAU.Module.Channels.DI.DITCReading': DIReading,
        'TAU.Module.Channels.DI.TimeTick': datetime,
    }

    return map
