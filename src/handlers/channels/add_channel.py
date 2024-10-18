from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from core.db import channels
from loader import dp, bot, list_of_channels
from states import States


@dp.callback_query_handler(text='yes', state=States.add_channel)
async def add_channel(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    channel_title = data['channel_title']
    channel_id = data['channel_id']
    link = data['link']

    channel_info = {
        'title': channel_title,
        'link': link,
        'id': channel_id,
        'caption': None
    }
    user_id = query.from_user.id
    await channels.add_channel(user_id, channel_info)
    user_channels = await channels.get_channels(user_id)
    keyboards.Channels.add_channel(keyboards.Channels(user_channels), channel_title, channel_id)

    await query.answer(f'Канал {channel_title} добавлен!', show_alert=False)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.set_state(None)



@dp.callback_query_handler(text='no', state=States.add_channel)
async def add_channel(query: types.CallbackQuery, state: FSMContext):
    await query.answer('Действие отменено', show_alert=False)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.set_state(None)
