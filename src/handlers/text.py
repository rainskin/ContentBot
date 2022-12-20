from aiogram import types

import texts
from loader import dp, bot


@dp.message_handler()
async def send_help(message: types.Message):
    await bot.send_message(message.chat.id, texts.commands)
