#!/usr/bin/env python3
"""0-basic_async_syntax.py module"""


import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
    Takes an int argument that waits for a random
    delay between o and max_delay and eventyally
    returns it.
    """
    waiting_time = random.random() * max_delay
    await asyncio.sleep(waiting_time)
    return waiting_time
