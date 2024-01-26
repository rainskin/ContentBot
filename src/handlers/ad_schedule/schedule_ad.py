from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

import config
from loader import dp, userbot
from states import States
from utils.time import create_valid_date


@dp.callback_query_handler(text='yes', state=States.schedule_ad)
async def add_admin(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(None)

    data = await state.get_data()
    day = data['day']
    hour = data['hour']
    minutes = data['minutes']

    date = create_valid_date(day)

    schedule_date = datetime(date.year, date.month, date.day, hour, minutes)

    channel_ids = data['channel_ids']

    msg_id = data['message_id'][0]


    await query.message.answer('Начинаю планирование')

    for channel_id in channel_ids:
        await userbot.forward_messages(channel_id, config.UPLOAD_CHANNEL_ID, msg_id, schedule_date=schedule_date, drop_author=True)
        # await userbot.copy(channel_id, None, schedule_date, msg_id)

    await query.message.answer('Закончил планирование')
    await state.finish()

@dp.callback_query_handler(text='no', state=States.check_channels)
async def add_admin(query: types.CallbackQuery, state: FSMContext):
    await query.answer('Действие отменено')
    await state.finish()
    await query.message.delete()