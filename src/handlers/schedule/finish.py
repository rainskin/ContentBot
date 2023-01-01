import asyncio
from datetime import datetime
from random import randint

from aiogram import types
from aiogram.dispatcher import FSMContext

import loader
from loader import dp, bot
from loader import other_channels, userbot
from states import States


@dp.callback_query_handler(state=States.accept)
async def finish(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chat = data['chat']
    chat_id = data['chat_id']
    days = data['days']
    time = data['time']
    collection = other_channels
    search_parameter = chat
    caption = ''
    anime_tyan = False
    total_photos_count = collection.count_documents({'channel': search_parameter})

    if chat == 'anime_tyan':
        collection = loader.ecchi_col
        search_parameter = 'url'
        anime_tyan = True
        caption = '__Channel:__ **[@anime4_tyan](https://t.me/+H2QjcBkVtcs4ZDNi)**'
        total_photos_count = collection.count_documents({})

    elif chat == 'hentai':
        collection = loader.hentai_coll
        search_parameter = 'url'
        anime_tyan = False
        total_photos_count = collection.count_documents({})

    elif chat == 'yuri':
        caption = '🎀 **[Yuri arts](https://t.me/+NTDsUr6Stvs3OWZi)**'

    requested_photos_count = len(days) * len(time)

    if requested_photos_count > total_photos_count:
        await bot.send_message(callback_query.message.chat.id,
                               f'В коллекции *{total_photos_count}* ты запросил {requested_photos_count}\nПополни '
                               f'коллекцию, либо выбери другие даты',
                               parse_mode=types.ParseMode.MARKDOWN)
    else:
        await bot.send_message(callback_query.message.chat.id, 'Начинаю планирование постов')
        for day in days:
            for hour in time:
                minute = randint(0, 8)
                date = datetime(year=datetime.now().year, month=datetime.now().month, day=day, hour=hour,
                                minute=minute)
                if chat == 'anime_tyan':
                    await userbot.schedule(chat_id, search_parameter, caption, date, anime_tyan)

                elif chat == 'hentai':
                    await userbot.schedule(chat_id, search_parameter, caption, date, anime_tyan=False)

                else:
                    await userbot.copy(chat_id, search_parameter, caption, date)
                await asyncio.sleep(0.1)

        await bot.send_message(callback_query.message.chat.id, 'Готово')
    await state.finish()