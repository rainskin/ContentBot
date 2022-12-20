import os

from aiogram import types

import config
from loader import bot, dp
from parser import Parser


@dp.message_handler(commands='auth')
async def cmd_setup(message: types.Message):
    if os.path.exists('cookies'):
        await message.answer('Авторизация уже пройдена, файл cookies найден')
    else:
        await message.answer('Прохожу авторизацию')
        Parser(config.path, config.username, config.password).authorization()
        await bot.send_message(message.chat.id, 'Готово')
