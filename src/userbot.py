from datetime import datetime
from typing import Any, Iterable, cast, Union

import pyrogram
from pyrogram import errors
from pyrogram.enums import ParseMode
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

import config
import loader


class Client(pyrogram.Client):
    def __init__(self, session_string: str):
        super().__init__('userbot', session_string=session_string)  # type: ignore

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
        r: Any = await self.invoke(  # type: ignore
            ForwardMessages(
                to_peer=await self.resolve_peer(chat_id),  # type: ignore
                from_peer=await self.resolve_peer(from_chat_id),  # type: ignore
                id=message_ids,
                silent=disable_notification or None,
                random_id=[self.rnd_id() for _ in message_ids],
                schedule_date=datetime_to_timestamp(schedule_date),
                noforwards=protect_content,
                drop_author=drop_author,
            )
        )
        forwarded_messages: list[Message] = []
        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}
        _types = UpdateNewMessage, UpdateNewChannelMessage, UpdateNewScheduledMessage
        for i in r.updates:
            if isinstance(i, _types):
                m = await Message._parse(self, i.message, users, chats)  # type: ignore
                forwarded_messages.append(cast(Message, m))
        return List(forwarded_messages) if is_iterable else forwarded_messages[0]

    async def delete_scheduled_messages(self, chat_id: int, msg_ids):
        r: Any = await self.invoke(DeleteScheduledMessages(peer=await self.resolve_peer(chat_id), id=msg_ids))


class Userbot:

    def __init__(self):
        self.app = Client(session_string=config.CH_SESSION_STRING)

    async def copy(self, chat_id, caption, date):
        app = self.app
        try:
            await app.start()
        except ConnectionError:
            pass

        # msg = loader.other_channels.find_one({'channel_id': chat_id})
        random_msg = loader.other_channels.aggregate(
            [{"$match": {"channel_id": chat_id}}, {"$sample": {"size": 1}}]).next()
        msg_id = random_msg['msg_id']

        try:
            # Для альбомов
            await app.copy_media_group(chat_id=chat_id, from_chat_id=config.UPLOAD_CHANNEL_ID, message_id=msg_id,
                                       captions=caption,
                                       schedule_date=date)
        except ValueError:
            # Для соло пикч
            await app.copy_message(chat_id=chat_id, from_chat_id=config.UPLOAD_CHANNEL_ID, message_id=msg_id,
                                   caption=caption,
                                   schedule_date=date)

        loader.other_channels.delete_one({'msg_id': msg_id})

    async def schedule(self, chat_id, search_parameter, caption, date, anime_tyan: bool):

        # Отложка для канала Аниме Тянки

        app = self.app

        try:
            await app.start()
        except ConnectionError:
            pass

        if anime_tyan:
            random_document = loader.ecchi_col.aggregate([{"$sample": {"size": 1}}]).next()
            photo_link = random_document[search_parameter]

            loader.ecchi_col.delete_one({'url': photo_link})
            loader.blacklist.insert_one({'url': photo_link})
            caption = ''

        else:
            random_document = loader.hentai_coll.aggregate([{"$sample": {"size": 1}}]).next()
            photo_link = random_document[search_parameter]
            loader.hentai_coll.delete_one({'url': photo_link})
            loader.blacklist.insert_one({'url': photo_link})
            caption = ''

        await app.send_photo(chat_id=chat_id, caption=caption, parse_mode=ParseMode.MARKDOWN, photo=photo_link,
                             schedule_date=date)

    async def in_chat(self, chat_id):

        app = self.app
        try:
            await app.start()
        except ConnectionError:
            pass

        try:
            return await self.app.get_chat(chat_id)
        except pyrogram.errors.ChannelInvalid:
            return False

    async def forward_messages(
            self,
            chat_id: int | str,
            from_chat_id: int | str,
            message_ids: int | Iterable[int],
            disable_notification: bool | None = None,
            schedule_date: datetime | None = None,
            protect_content: bool | None = None,
            drop_author: bool | None = None,
    ):
        app = self.app
        try:
            await app.start()
        except ConnectionError:
            pass

        messages = await app.forward_messages(chat_id, from_chat_id, message_ids, disable_notification, schedule_date,
                                              protect_content, drop_author)

        grouped_messages = {}
        pp = []
        for msg in messages:
            chat_id = msg.chat.id
            if chat_id not in grouped_messages.keys():
                grouped_messages[chat_id] = []
                grouped_messages[chat_id].append(msg.id)

            else:
                grouped_messages[chat_id].append(msg.id)

            pp.append(grouped_messages)

        result = [(chat_id, msgs) for chat_id, msgs in grouped_messages.items()]
        return result

    async def delete_ad_posts(self, chat_id: int, link: str):
        """
        Deletes all messages from the channel that include a link

        :param chat_id:
        :param link:
        :return:
        """

        app = self.app
        try:
            await app.start()
        except ConnectionError:
            pass

        msg_ids = []

        async for msg in app.search_messages(chat_id, link, limit=10):
            new_msg_ids = await self.get_msg_ids(chat_id, msg.id)
            msg_ids += new_msg_ids

        await app.delete_messages(chat_id, msg_ids)

    async def delete_ad_posts2(self, chat_id: int, query: str):
        """
        Deletes all messages from the channel that include a link

        :param chat_id:
        :param query: link to search
        :return:
        """

        app = self.app
        try:
            await app.start()
        except ConnectionError:
            pass

        msg_ids = []

        async for msg in app.get_chat_history(chat_id, 150):
            entities = msg.entities

            if not msg.entities:
                continue

            text = msg.text or msg.caption

            for entity in entities:
                if entity.type == 'text_link':
                    url = entity.url
                elif entity.type == 'url':
                    url = text[entity.offset:entity.offset + entity.length]
                else:
                    return

                if query != url:
                    return

                new_msg_ids = await self.get_msg_ids(chat_id, msg.id)
                msg_ids += new_msg_ids

        await app.delete_messages(chat_id, msg_ids)

    async def get_messages(
            self,
            chat_id: Union[int, str],
            message_ids: Union[int, Iterable[int]] = None,
            reply_to_message_ids: Union[int, Iterable[int]] = None,
            replies: int = 1
    ) -> Union["pyrogram.types.Message", List["pyrogram.types.Message"]]:
        app = self.app
        try:
            await app.start()
        except ConnectionError:
            pass

        return await app.get_messages(chat_id, message_ids, reply_to_message_ids, replies)

    async def get_msg_ids(self, chat_id: int, msg_id: int):

        app = self.app
        try:
            await app.start()
        except ConnectionError:
            pass

        msg = await app.get_messages(chat_id, msg_id)
        msg_ids = []
        if msg.media_group_id:

            for m_msg in await app.get_media_group(chat_id, msg.id):
                msg_ids.append(m_msg.id)

        else:
            msg_ids.append(msg.id)

        return msg_ids

    async def delete_scheduled_messages(self, chat_id: int, msg_ids):
        app = self.app
        try:
            await app.start()
        except ConnectionError:
            pass

        await app.delete_scheduled_messages(chat_id, msg_ids)


userbot = Userbot()
