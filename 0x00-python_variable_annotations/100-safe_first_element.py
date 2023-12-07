#!/usr/bin/env python3
"""100-safe_first_element module"""
from typing import Sequence, Any, Union


"""The types of the elements of the input are not know"""


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Retrieves the first element of a sequence if it exists."""
    if lst:
        return lst[0]
    else:
        return None
