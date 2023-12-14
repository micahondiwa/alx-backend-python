#!/usr/bin/env python3
""" 2-measure_runtime """
import time
import asyncio

async_comprehension = __import__("1-async_comprehension").async_comprehension


async def measure_runtime() -> float:
    """
    Executes async_comprehension four times in parallel using
    asyncio.gather and returns the total runtime.
    """
    start = time.time()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    end = time.time()
    return end - start
