import os

from aiogram import types

import config
import image
from loader import bot, dp, ecchi_col
from parser import Parser


@dp.message_handler(commands='parse')
async def cmd_parse(message: types.Message):
    if os.path.exists('cookies'):
        await bot.send_message(message.chat.id, 'Начинаю парсить')
        links = Parser(config.path, config.username, config.password).get_images(config.url)

        await bot.send_message(message.chat.id, 'Закончил')
        await bot.send_message(message.chat.id, 'Добавляю в дб')
        links_amount = []

        for url in links:
            item = {
                'url': url
            }
            if image.is_new(url) is True:
                ecchi_col.insert_one(item)
                links_amount.append(item)

        await bot.send_message(message.chat.id, f'Количество новых пикч: {len(links_amount)}')
    else:
        await bot.send_message(message.chat.id, 'Сначала нужно пройти авторизацию. Жми /auth')
