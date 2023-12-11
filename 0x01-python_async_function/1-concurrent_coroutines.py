#!/usr/bin/env python3
"""1-concurrent_coroutines.py"""

from typing import List
import asyncio

wait_random = __import__("0-basic_async_syntax").wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    With a specified max_delay and returns the list
    of all the delauys (float values) in ascending
    order.
    """
    delay = await asyncio.gather(*[wait_random(max_delay) for i in range(n)])
    return sorted(delay)
