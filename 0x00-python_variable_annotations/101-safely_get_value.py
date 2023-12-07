#!/usr/bin/env python3
"""101-safely_get_value module"""
from typing import Mapping, Union, Any, TypeVar

T = TypeVar("T")
Res = Union[Any, T]
Def = Union[T, None]


def safely_get_value(dct: Mapping, key: Any, default: Def = None) -> Res:
    """
    Retrieves a value from a dict using a given key.
    """
    if key in dct:
        return dct[key]
    else:
        return default
