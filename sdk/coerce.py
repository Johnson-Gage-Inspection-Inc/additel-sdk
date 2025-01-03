from datetime import datetime
from typing import List
import re

def coerce(adt: dict, map: dict = None):
    """
    Dynamically coerces a dictionary-based object to its appropriate type
    using a provided type mapping.

    Args:
        adt (dict): The dictionary containing the Additel-formatted data to coerce.
        map (dict): A mapping of type strings to Python types/classes.
        date_format (str): Optional format string for parsing datetime objects.

    Returns:
        An instance of the type determined from the `$type` key in the dictionary.

    Raises:
        TypeError: If `$type` is missing or not recognized in the provided map.
    """
    if not map:
        map = load_mapping()
    if not isinstance(adt, dict):
        return adt
    typeStr = adt.pop('$type', None)
    if typeStr is None:
        return adt
    listIndicator = r'System\.Collections\.Generic\.List`1\[\[([\w\.]+), ([\w\.]+)\]\], ([\w\.]+)'
    if match := re.match(listIndicator, typeStr):
        type = List[map[match.group(1)]]
        adt = adt['$values']
        return [coerce(v, map) if isinstance(v, dict) else v for v in adt]
    else:
        typeStr, _ = typeStr.split(',')
        type = map[typeStr]

    if typeStr not in map:
        raise TypeError(f"Unknown type: {typeStr}. Full map: {map}")

    # Handle date formatting
    if type == datetime:
        return datetime.strptime(adt['TickTime'], '%Y-%m-%d %H:%M:%S %f')

    # Recursively coerce nested dictionaries:
    for key, value in adt.items():
        if isinstance(value, dict):
            adt[key] = coerce(value, map)
        elif isinstance(value, list):
            adt[key] = [coerce(v, map) for v in value]

    return type(**adt)

def load_mapping():
    from .customTypes import DI
    map = {
        'System.Double': float,
        'TAU.Module.Channels.DI.DIFunctionChannelConfig': DI.DIFunctionChannelConfig,
        'TAU.Module.Channels.DI.DIScanInfo': DI.DIScanInfo,
        'TAU.Module.Channels.DI.DIModuleInfo': DI.DIModuleInfo,
        'TAU.Module.Channels.DI.DIReading': DI.DIReading,
        'TAU.Module.Channels.DI.DITemperatureReading': DI.DIReading,
        'TAU.Module.Channels.DI.DIElectricalReading': DI.DIReading,
        'TAU.Module.Channels.DI.DITCReading': DI.DIReading,
        'TAU.Module.Channels.DI.TimeTick': datetime,
    }

    return map
