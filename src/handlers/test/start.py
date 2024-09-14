from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from pyrogram.enums import ParseMode

import keyboards
from loader import dp, bot, userbot
from states import States
from utils.check_admin_rights import is_superadmin
from utils.time import get_current_datetime
import re


@dp.message_handler(commands='test')
async def cmd_test(msg: types.Message, state: FSMContext):
    if not is_superadmin(msg.from_user.id):
        return

    # await userbot.create_tests(bot.id)
    await state.set_state(States.test)
    await msg.answer('test', reply_markup=keyboards.test_kb)


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
