#!/usr/bin/env python3
"""0-basic_async_syntax.py
"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
    waits for a random delay between 0
    and max_delay
    (included and float value)
    seconds and eventually returns it.
    """
    random_wait_time = random.random() * max_delay
    await asyncio.sleep(random_wait_time)
    return random_wait_time
