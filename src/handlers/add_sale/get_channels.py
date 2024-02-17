from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, list_of_channels
from states import States
from utils import links


@dp.message_handler(state=States.get_channels_for_ad)
async def _(msg: types.Message, state: FSMContext):
    if not msg.entities:
        await msg.answer('Отправь сообщение, содержащее ссылки на канал')
        return

    channel_links = await links.get_links_from_msg(msg)

    channels = []
    channel_ids = []

    channel_serial_number = 0
    for link in channel_links:
        channel = list_of_channels.find_one({'link': link})
        if not channel:
            continue

        channel_serial_number += 1
        title = channel['title']
        _id = channel['id']
        channel_ids.append(_id)
        channels.append(str(channel_serial_number) + '. ' + title)

    if not channels:
        await msg.answer('Ты не выбрал каналы')
        return

    channel_text = "\n".join(channels)
    text = f'Выбраны следующие каналы:\n\n<b>{channel_text}</b>\n\nВсе верно?'
    await msg.answer(text, parse_mode='html', reply_markup=keyboards.YesOrNo())

    await state.update_data(channels=channels, channel_ids=channel_ids, channel_links=channel_links)
    await States.check_channels.set()



