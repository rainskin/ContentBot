import asyncio
from typing import Any, Awaitable
import config

from pyrogram.client import Client


def run(coro: Awaitable[Any]):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coro)


async def main():
    client = Client("choch", config.API_ID, config.API_HASH)
    print(client)

    async with client:
        result = await client.export_session_string()
        print(result)

run(main())
