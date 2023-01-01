from aiogram import types

import texts
from loader import dp, bot


@dp.message_handler()
async def send_help(msg: types.Message):
    if msg.from_user.id != 936845322:
        await msg.answer('Нет доступа')
    else:
        await bot.send_message(msg.chat.id, texts.commands)

