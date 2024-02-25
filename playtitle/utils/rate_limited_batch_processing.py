import asyncio
from typing import Coroutine


async def exec_with_semaphore(coroutine: Coroutine, semaphore: asyncio.Semaphore):
    async with semaphore:
        return await coroutine


async def rate_limited_batch_processing(coroutines, max_concurrent_batches: int):
    semaphore = asyncio.Semaphore(max_concurrent_batches)
    return await asyncio.gather(
        *[exec_with_semaphore(coroutine, semaphore) for coroutine in coroutines]
    )
