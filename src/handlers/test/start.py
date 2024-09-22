import re

import pyrogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from pyrogram.storage.sqlite_storage import get_input_peer

from loader import dp, userbot
from states import States
from utils.check_admin_rights import is_superadmin


@dp.message_handler(commands='test')
async def cmd_test(msg: types.Message, state: FSMContext):
    if not is_superadmin(msg.from_user.id):
        return


@dp.message_handler(state=States.test, content_types=ContentType.ANY)
async def _(msg: types.Message, state: FSMContext):
    text = replace_emoji_tags(msg.html_text)
    print(text)
    await userbot.send_message('me', text)


def replace_emoji_tags(msg_html_text: str):
    return re.sub(
        r'<tg-emoji emoji-id="(.*?)">(.*?)</tg-emoji>',
        r'<emoji id=\1>\2</emoji>',
        msg_html_text,
    )


# <tg-emoji emoji-id="6152103458209007684">☺️</tg-emoji>


async def get_all_peers(storage):
    # Извлекаем все пиры из базы данных
    peers = storage.conn.execute("SELECT id, access_hash, type FROM peers").fetchall()

    if not peers:
        print("No peers found in storage")
        return []

    return [get_input_peer(*peer) for peer in peers]
