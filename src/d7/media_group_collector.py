import asyncio
from collections import defaultdict
from aiogram import types

MESSAGES_BY_GROUP: dict[int, list[types.Message]] = defaultdict(list)


async def collect_media_group(msg: types.Message) -> list[types.Message]:
    group_id = msg.media_group_id
    if not group_id:
        return [msg]
    messages = MESSAGES_BY_GROUP[group_id]
    messages.append(msg)
    if len(messages) > 1:
        return []
    await asyncio.sleep(1)
    del MESSAGES_BY_GROUP[group_id]
    return messages
