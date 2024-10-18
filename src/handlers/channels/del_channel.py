from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from core.db import channels
from loader import dp, bot, list_of_channels
from states import States


@dp.callback_query_handler(text='del_channel', state=States.channel_management)
async def _(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    user_channels = await channels.get_channels(user_id)
    await bot.send_message(query.message.chat.id, 'Нажми на канал, который хочешь удалить',
                           reply_markup=keyboards.Channels(user_channels))
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.answer()
    await States.choose_channel_for_delete.set()


@dp.callback_query_handler(state=States.choose_channel_for_delete)
async def choose_channel(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    channel_id = int(query.data)
    channel = await channels.get_channel_by_id(channel_id)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await bot.send_message(query.message.chat.id, f"Удалить канал <b>{channel['title']}</b> ?", parse_mode='html',
                           reply_markup=keyboards.YesOrNo())
    await state.update_data(channel_id=channel_id)
    await query.answer()
    await States.del_channel.set()


@dp.callback_query_handler(text='yes', state=States.del_channel)
async def delete_channel(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    data = await state.get_data()
    channel_id = data['channel_id']
    await channels.remove_channel(user_id, channel_id)
    user_channels = await channels.get_channels(user_id)
    keyboards.Channels.delete_channel(keyboards.Channels(user_channels), channel_id)
    await query.answer('Канал удалён!', show_alert=True)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.set_state(None)


@dp.callback_query_handler(text='no', state=States.del_channel)
async def _(query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await bot.send_message(query.message.chat.id, 'Действие отменено')
    await query.answer()
    await state.set_state(None)
