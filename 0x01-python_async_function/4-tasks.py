#!/usr/bin/env python3
"""4-tasks.py"""

from typing import List
import asyncio

task_wait_random = __import__("3-tasks").task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Async function that executes task_wait_random n times with the
    specified max_delay and returns the list of all the
    delays (float) in ascending.
    """
    delays = await asyncio.gather(
        *[task_wait_random(max_delay) for i in range(n)])
    return sorted(delays)
