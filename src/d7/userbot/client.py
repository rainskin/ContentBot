from datetime import datetime
from typing import Iterable, cast
import pyrogram
from pyrogram.raw.functions.messages.forward_messages import ForwardMessages
from pyrogram.raw.functions.messages import DeleteScheduledMessages
from pyrogram.raw.types import (
    UpdateNewChannelMessage,
    UpdateNewMessage,
    UpdateNewScheduledMessage,
)
from pyrogram.types import Message
from pyrogram.types.list import List
from pyrogram.utils import datetime_to_timestamp


class Client(pyrogram.Client):
    async def forward_messages(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_ids: int | Iterable[int],
        disable_notification: bool | None = None,
        schedule_date: datetime | None = None,
        protect_content: bool | None = None,
        drop_author: bool | None = None,
    ) -> Message | list[Message]:
        is_iterable = not isinstance(message_ids, int)
        message_ids = list(message_ids) if is_iterable else [message_ids]
        query = ForwardMessages(
            to_peer=await self.resolve_peer(chat_id),
            from_peer=await self.resolve_peer(from_chat_id),
            id=message_ids,
            silent=disable_notification or None,
            random_id=[self.rnd_id() for _ in message_ids],
            schedule_date=datetime_to_timestamp(schedule_date),
            noforwards=protect_content,
            drop_author=drop_author,
        )
        resp = await self.invoke(query)
        forwarded_messages: list[Message] = []
        users = {i.id: i for i in resp.users}
        chats = {i.id: i for i in resp.chats}
        _types = UpdateNewMessage, UpdateNewChannelMessage, UpdateNewScheduledMessage
        for i in resp.updates:
            if isinstance(i, _types):
                _msg = await Message._parse(self, i.message, users, chats)
                msg = cast(Message, _msg)
                forwarded_messages.append(msg)
        return List(forwarded_messages) if is_iterable else forwarded_messages[0]

    async def delete_scheduled_messages(self, chat_id: int, message_ids: list[int]):
        peer = await self.resolve_peer(chat_id)
        query = DeleteScheduledMessages(peer=peer, id=message_ids)
        await self.invoke(query)
