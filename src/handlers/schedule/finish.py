import asyncio
from datetime import datetime
from random import randint

from aiogram import types
from aiogram.dispatcher import FSMContext

import loader
from loader import dp, bot
from loader import other_channels, userbot
from states import States
from utils.time import create_valid_date, one_day, current_day, current_hour


@dp.callback_query_handler(state=States.accept)
async def finish(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    channel_name = str(data['channel_name'])
    channel_id = data['channel_id']
    days = data['days']
    time = data['time']

    first_date = create_valid_date(days[0])

    if len(days) == 2:
        second_date = create_valid_date(days[1]) or first_date
    else:
        second_date = first_date

    date = first_date

    collection = other_channels
    search_parameter = channel_id

    total_photos_count = collection.count_documents({'channel_id': search_parameter})

    if 'anime tyans' in channel_name.lower():
        collection = loader.ecchi_col
        total_photos_count = collection.count_documents({})

    elif 'vip tyan' in channel_name.lower():
        collection = loader.hentai_coll
        total_photos_count = collection.count_documents({})

    amount_of_days = second_date.day - first_date.day + 1

    requested_posts_count = amount_of_days * len(time) - calculate_dropped_posts(first_date, time)

    if requested_posts_count > total_photos_count:
        await bot.send_message(callback_query.message.chat.id,
                               f'В коллекции *{total_photos_count}* ты запросил {requested_posts_count}\nПополни '
                               f'коллекцию, либо выбери другие даты',
                               parse_mode=types.ParseMode.MARKDOWN)
    else:
        await bot.send_message(callback_query.message.chat.id, 'Начинаю планирование постов')

        while date <= second_date:
            await schedule_posts(date, time, channel_name, channel_id)
            date += one_day

        await bot.send_message(callback_query.message.chat.id, 'Готово')

    await state.finish()


async def schedule_posts(date: datetime, time: list, channel_name: str, channel_id: int):
    year = date.year
    month = date.month
    day = date.day

    caption = None
    search_parameter = 'url'  # for tyan and vip tyan
    for hour in time:

        if date.day == current_day and current_hour > hour:
            continue

        minute = randint(0, 8)
        schedule_date = datetime(year=year, month=month, day=day, hour=hour, minute=minute)

        if 'anime tyans' in channel_name.lower():
            await userbot.schedule(channel_id, search_parameter, caption, schedule_date, anime_tyan=True)

        elif 'vip tyan' in channel_name.lower():
            await userbot.schedule(channel_id, search_parameter, caption, schedule_date, anime_tyan=False)

        else:
            await userbot.copy(channel_id, caption, schedule_date)
        await asyncio.sleep(0.1)


def calculate_dropped_posts(date: datetime, time: list[int]):
    dropped_posts = 0

    for hour in time:
        if date.day == current_day and current_hour > hour:
            dropped_posts += 1

    return dropped_posts
