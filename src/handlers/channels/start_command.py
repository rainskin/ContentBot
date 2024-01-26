from aiogram import types
from aiogram.dispatcher import FSMContext
from pyrogram.raw.types import MessageEntityCustomEmoji

import keyboards
from states import States
from loader import dp, list_of_channels, bot
from utils.check_admin_rights import is_superadmin


@dp.message_handler(commands='channels')
async def _(msg: types.Message, state: FSMContext):
    if not is_superadmin(msg.from_user.id):
        await msg.answer('Нет доступа')
    else:
        channels = await msg.answer('Список каналов', reply_markup=keyboards.ChannelsWithServiceButtons())
        await States.channel_management.set()
        await state.update_data(channels=channels.message_id)


def show_channels():
    ids = list_of_channels.distinct('id')
    channels = dict()
    for _id in ids:
        channel = list_of_channels.find_one({'id': _id})
        channels[channel['title']] = {
            'id': channel['id']
        }

    return channels


@dp.callback_query_handler(text='cancel', state=States.channel_management)
async def cancel(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(query.message.chat.id, 'Операция отменена')
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.answer()
    await state.set_state(None)
