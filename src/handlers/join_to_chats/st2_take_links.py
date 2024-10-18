import asyncio
import random

from aiogram import types
import json

from aiogram.dispatcher import FSMContext

from config import USERBOT_ID
from core.db import channels
from loader import dp, userbot, bot
from pyrogram.errors import RPCError
from pyrogram.errors import exceptions
from pyrogram.types.user_and_chats import ChatPermissions
from pyrogram.types.user_and_chats import Chat as PyrogramChat

from states import States


@dp.message_handler(state=States.waiting_chat_links)
async def _(msg: types.Message, state: FSMContext) -> None:

    user_id = msg.from_user.id
    count = 0
    user_channels = await channels.get_channels(user_id)

    for channel_info in user_channels:
        channel_id = channel_info.get('id')
        userbot_status = await channels.get_userbot_status(channel_id)

        if userbot_status:
            continue

        channel_link = channel_info.get('link')
        channel_id = channel_info.get('id')
        channel_title = channel_info.get('title')
        link = make_invite_link(channel_link)
        channel_name_with_link = f'<a href="{link}">{channel_title}</a>'
        message = await msg.answer(f'⌛Пробую подписаться на {channel_name_with_link}')

        try:
            await bot.get_chat_administrators(channel_id)
        except Exception as e:
            continue

        try:
            await userbot.app.join_chat(link)
        except exceptions.InviteHashExpired:
            await msg.answer(f'❌ Ссылка: {link} не работает')
            return
        except (RPCError, KeyError) as e:
            await msg.answer(f'Не удалось подписаться на {channel_name_with_link}.\n\n{e}')
            continue

        except Exception as e:
            await msg.answer(f'что-то пошло не так\n\n{e}')
            return

        count += 1

        await msg.answer(f'✅ Подписался на {channel_name_with_link}')

        admin_rights = {
            "can_delete_messages": True,
            "can_edit_messages": True,
            "can_post_messages": True
        }

        try:
            await bot.promote_chat_member(channel_id, USERBOT_ID, **admin_rights)
        except Exception as e:
            await msg.answer(f'Не удалось дать права администратор в канале {channel_name_with_link}.\n\n{e}')
            break
        await channels.set_userbot_status(channel_id, True)
        timeout = random.randint(0,  10)
        await message.edit_text(f'Сплю {timeout} секунд')
        await asyncio.sleep(timeout)

    text = f'Подписался на {count} чат(ов)'
    await msg.answer(text)
    await state.set_state(None)


def _parse_entity(text: str, entity: types.MessageEntity) -> str | None:
    url = None

    if entity.type == 'text_link':
        url = entity.url
    elif entity.type == 'mention':
        url = 'https://t.me/' + text[entity.offset + 1:entity.offset + entity.length]
    elif entity.type == 'url':
        url = text[entity.offset:entity.offset + entity.length]

    if not url or 't.me' not in url:
        return None

    if not url.startswith('http'):
        url = 'https://' + url

    return url.replace('http://', 'https://')


def parse_urls(msg: types.Message) -> list[str]:
    text = msg.text or msg.caption
    entities = msg.entities or msg.caption_entities or []
    urls_raw = {_parse_entity(text, e) for e in entities}
    return [i for i in urls_raw if i]


def is_chat_link_private(url: str) -> bool:
    """
    :param url:
    :return: the link only if this is a closed type telegram chat
    """
    return url.startswith('https://t.me/+') or url.startswith('https://t.me/%')


def is_chat_link_private_old_type(url: str) -> bool:
    return url.startswith('http://t.me/joinchat/')


def is_chat_link_invite_type(url: str) -> bool:
    return url.startswith('https://t.me/%2B')


def make_invite_link(url: str) -> str:
    """
    :param url:
    :return: returns the correct invite link depending on the chat type
    """
    if is_chat_link_private_old_type(url):
        return url
    elif is_chat_link_invite_type(url):
        return url.replace('https://t.me/%2B', 'https://t.me/+')
    else:
        return url.removeprefix('https://t.me/') if not is_chat_link_private(url) else url


def parse_permissions(obj: ChatPermissions) -> dict:
    """
    get permissions from json without first pare of key and value
    :param obj:
    :return: new dict
    """
    data = dict(json.loads(str(obj)))
    return {key: item for key, item in data.items() if 'can' in key}


def get_chat_data(chat: PyrogramChat, url: str) -> dict:
    """
    Collects and prepares all chat data before adding to the db
    :param chat: PyrogramChat object
    :param url: just url
    :return: dictionary with data
    """
    title = chat.title
    chat_id = chat.id
    permissions = list(parse_permissions(chat.permissions).items())
    data = [('title', title), ('chat_id', chat_id), ('url', url)] + permissions
    return dict(data)
