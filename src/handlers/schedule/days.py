from aiogram import types
from aiogram.dispatcher import FSMContext

import config
from loader import dp, ecchi_col, yuri, cute_pics, userbot
from states import States


@dp.message_handler(state=States.choosing_days)
async def schedule(message: types.Message, state: FSMContext):
    period = message.text.split(' ')
    first_day = int(period[0])
    last_day = int(period[1])
    days = list(range(first_day, last_day + 1))
    time = [10, 11, 13]
    data = await state.get_data()
    chat = data['chat']
    chat_id = data['chat_id']
    collection = ''
    if chat == 'anime_tyan':
        collection = ecchi_col

    elif chat == 'yuri':
        collection = yuri

    elif chat == 'cute_pics':
        collection = cute_pics

    await userbot.schedule(config.TEST_CHANNEL_ID, collection, days, time)
