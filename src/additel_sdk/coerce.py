from .time import TimeTick
from typing import List, Union, Any
import re
from json import loads
from .registry import TYPE_REGISTRY


def coerce(adt: Union[dict, str, list]) -> Any:
    """
    Dynamically coerces a dictionary-based object to its appropriate type
    using a provided type mapping.

    Args:
        adt (dict or str): The Additel-formatted data to coerce
        date_format (str): Optional format string for parsing datetime objects.

    Returns:
        An instance of the type determined from the `$type` key in the dictionary.

    Raises:
        TypeError: If `$type` is missing or not recognized in the provided map.
    """

    def coerce_list(adt: list):
        return [coerce(v) if isinstance(v, dict) else v for v in adt]

    if isinstance(adt, list):
        return coerce_list(adt, TYPE_REGISTRY)

    if isinstance(adt, str):
        adt = loads(adt)

    typeStr = adt.pop("$type", None)
    if not typeStr:
        # Prevent an infinite loop by returning the dictionary if no type is specified
        return adt

    ClassName = adt.pop("ClassName", None)  # noqa: F841
    listIndicator = re.compile(r"""
        System\.Collections\.Generic\.List`1\[\[   # Outer List
        ([\w\.]+),\s+                              # Type name
        ([\w\.]+)\]\],\s+                          # Namespace
        ([\w\.]+)                                  # Assembly
    """, re.VERBOSE)
    if match := re.match(listIndicator, typeStr):
        typ = List[TYPE_REGISTRY[match.group(1)]]
        adt = adt["$values"]
        return coerce_list(adt)

    typeStr0 = typeStr.split(",")[0]

    if typ := TYPE_REGISTRY.get(typeStr0, None):
        for key, value in adt.items():
            if isinstance(value, dict):
                adt[key] = coerce(value)
            elif isinstance(value, list):
                adt[key] = [coerce(v) for v in value]

        return typ(**adt)  # Instantiate the type with the coerced dictionary
    raise TypeError(f"Type not found in mapping: {typeStr0}")


def load_mapping():
    from . import channel, module, scan

    return {
        "System.Double": float,
        "TAU.Module.Channels.DI.DIFunctionVoltageChannelConfig":
            channel.DIFunctionVoltageChannelConfig,
        "TAU.Module.Channels.DI.DIFunctionCurrentChannelConfig":
            channel.DIFunctionCurrentChannelConfig,
        "TAU.Module.Channels.DI.DIFunctionResistanceChannelConfig":
            channel.DIFunctionResistanceChannelConfig,
        "TAU.Module.Channels.DI.DIFunctionRTDChannelConfig":
            channel.DIFunctionRTDChannelConfig,
        "TAU.Module.Channels.DI.DIFunctionThermistorChannelConfig":
            channel.DIFunctionThermistorChannelConfig,
        "TAU.Module.Channels.DI.DIFunctionTCChannelConfig":
            channel.DIFunctionTCChannelConfig,
        "TAU.Module.Channels.DI.DIFunctionSwitchChannelConfig":
            channel.DIFunctionSwitchChannelConfig,
        "TAU.Module.Channels.DI.DIFunctionSPRTChannelConfig":
            channel.DIFunctionSPRTChannelConfig,
        "TAU.Module.Channels.DI.DIFunctionVoltageTransmitterChannelConfig":
            channel.DIFunctionVoltageTransmitterChannelConfig,
        "TAU.Module.Channels.DI.DIFunctionCurrentTransmitterChannelConfig":
            channel.DIFunctionCurrentTransmitterChannelConfig,
        "TAU.Module.Channels.DI.DIFunctionStandardTCChannelConfig":
            channel.DIFunctionStandardTCChannelConfig,
        "TAU.Module.Channels.DI.DIFunctionCustomRTDChannelConfig":
            channel.DIFunctionCustomRTDChannelConfig,
        "TAU.Module.Channels.DI.DIFunctionStandardResistanceChannelConfig":
            channel.DIFunctionStandardResistanceChannelConfig,
        "TAU.Module.Channels.DI.DIFunctionChannelConfig":
            channel.DIFunctionChannelConfig,
        "TAU.Module.Channels.DI.DIScanInfo": scan.DIScanInfo,
        "TAU.Module.Channels.DI.DIModuleInfo": module.DIModuleInfo,
        "TAU.Module.Channels.DI.DIReading": scan.DIReading,
        "TAU.Module.Channels.DI.DITemperatureReading": scan.DITemperatureReading,
        "TAU.Module.Channels.DI.DIElectricalReading": scan.DIElectricalReading,
        "TAU.Module.Channels.DI.DITCReading": scan.DITCReading,
        "TAU.Module.Channels.DI.TimeTick": TimeTick,
    }
