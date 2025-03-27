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

    def _coerce_list(adt: list):
        return [coerce(v) if isinstance(v, dict) else v for v in adt]

    if isinstance(adt, list):
        return _coerce_list(adt)

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
        return _coerce_list(adt)

    typeStr0 = typeStr.split(",")[0]

    if typ := TYPE_REGISTRY.get(typeStr0, None):
        for key, value in adt.items():
            if isinstance(value, dict):
                adt[key] = coerce(value)
            elif isinstance(value, list):
                adt[key] = _coerce_list(value)

        return typ(**adt)  # Instantiate the type with the coerced dictionary
    raise TypeError(f"Type not found in mapping: {typeStr0}")
