from aiogram import types
from aiogram.dispatcher import FSMContext
from pyrogram.raw.types import MessageEntityCustomEmoji

from core.db import channels
import keyboards
from states import States
from loader import dp, list_of_channels, bot
from utils.check_admin_rights import is_superadmin, is_admin


@dp.message_handler(commands='channels')
async def _(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    if not is_superadmin(user_id) and not is_admin(user_id):
        await msg.answer('Нет доступа')
        return

    user_channels = await channels.get_channels(user_id)
    msg_with_channels = await msg.answer('Список каналов', reply_markup=keyboards.ChannelsWithServiceButtons(user_channels))
    await States.channel_management.set()
    await state.update_data(msg_with_channels_id=msg_with_channels.message_id)


@dp.callback_query_handler(text='add_channel', state=States.channel_management)
async def _(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_with_channels_id = data['msg_with_channels_id']
    text = (f'Чтобы добавить новый канал:\n\n'
            f'1. Добавь меня в администраторы канала с правами на управление сообщениями и назначение администраторов '
            f'(это необходимо для автоматического добавления юзербота)\n'
            f'2. Перешли сюда сообщение с канала, который хочешь добавить. Это не должен быть альбом')
    await bot.send_message(query.message.chat.id, text)
    await bot.delete_message(query.message.chat.id, msg_with_channels_id)
    await query.answer()
    await States.get_channel_data.set()


@dp.callback_query_handler(text='cancel', state=States.channel_management)
async def cancel(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(query.message.chat.id, 'Операция отменена')
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.answer()
    await state.set_state(None)
