from typing import List, Union
import re
import logging


def coerce(adt: Union[dict, str, list], map: dict = None):
    """
    Dynamically coerces a dictionary-based object to its appropriate type
    using a provided type mapping.

    Args:
        adt (dict or str): The Additel-formatted data to coerce
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

    if typeStr := adt.pop("$type", None):
        ClassName = adt.pop("ClassName", None)  # noqa: F841
        listIndicator = r"System\.Collections\.Generic\.List`1\[\[([\w\.]+), ([\w\.]+)\]\], ([\w\.]+)"  # noqa: E501
        if match := re.match(listIndicator, typeStr):
            typ = List[map[match.group(1)]]
            adt = adt["$values"]
            return coerce_list(adt, map)

        typeStr = typeStr.split(",")[0]
        typ = map.get(typeStr, None)
        if typ is None:
            raise TypeError(f"Unknown type: {typeStr}. Full map: {map}")

        # Recursively coerce nested dictionaries:
        for key, value in adt.items():
            if isinstance(value, dict):
                adt[key] = coerce(value, map)
            elif isinstance(value, list):
                adt[key] = [coerce(v, map) for v in value]

        return typ(**adt)  # Instantiate the type with the coerced dictionary

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
    from .channel import DI

    return {
        "System.Double": float,
        "TAU.Module.Channels.DI.DIFunctionVoltageChannelConfig": DI.DIFunctionVoltageChannelConfig,  # - 0: Voltage
        "TAU.Module.Channels.DI.DIFunctionCurrentChannelConfig": DI.DIFunctionCurrentChannelConfig,  # - 1: Current
        "TAU.Module.Channels.DI.DIFunctionResistanceChannelConfig": DI.DIFunctionResistanceChannelConfig,  # - 2: Resistance
        "TAU.Module.Channels.DI.DIFunctionRTDChannelConfig": DI.DIFunctionRTDChannelConfig,
        "TAU.Module.Channels.DI.DIFunctionThermistorChannelConfig": DI.DIFunctionThermistorChannelConfig,  # - 4: Thermistor
        "TAU.Module.Channels.DI.DIFunctionTCChannelConfig": DI.DIFunctionTCChannelConfig,  # - 100: Thermocouple (TC)
        "TAU.Module.Channels.DI.DIFunctionSwitchChannelConfig": DI.DIFunctionSwitchChannelConfig,  # - 101: Switch
        "TAU.Module.Channels.DI.DIFunctionSPRTChannelConfig": DI.DIFunctionSPRTChannelConfig,  # - 102: SPRT
        "TAU.Module.Channels.DI.DIFunctionVoltageTransmitterChannelConfig": DI.DIFunctionVoltageTransmitterChannelConfig,  # - 103: Voltage Transmitter
        "TAU.Module.Channels.DI.DIFunctionCurrentTransmitterChannelConfig": DI.DIFunctionCurrentTransmitterChannelConfig,  # - 104: Current Transmitter
        "TAU.Module.Channels.DI.DIFunctionStandardTCChannelConfig": DI.DIFunctionStandardTCChannelConfig,  # - 105: Standard TC
        "TAU.Module.Channels.DI.DIFunctionCustomRTDChannelConfig": DI.DIFunctionCustomRTDChannelConfig,  # - 106: Custom RTD
        "TAU.Module.Channels.DI.DIFunctionStandardResistanceChannelConfig": DI.DIFunctionStandardResistanceChannelConfig,  # - 110: Standard Resistance
        "TAU.Module.Channels.DI.DIFunctionChannelConfig": DI.DIFunctionChannelConfig,
        "TAU.Module.Channels.DI.DIScanInfo": DI.DIScanInfo,
        "TAU.Module.Channels.DI.DIModuleInfo": DI.DIModuleInfo,
        "TAU.Module.Channels.DI.DIReading": DI.DIReading,
        "TAU.Module.Channels.DI.DITemperatureReading": DI.DITemperatureReading,
        "TAU.Module.Channels.DI.DIElectricalReading": DI.DIElectricalReading,
        "TAU.Module.Channels.DI.DITCReading": DI.DITCReading,
        "TAU.Module.Channels.DI.TimeTick": DI.TimeTick,
    }
