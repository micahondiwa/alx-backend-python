#!/usr/bin/env python3
"""9-element_length module"""
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Annotates the function's parameters and return
    values with the appropriate types
    """
    return [(i, len(i)) for i in lst]
