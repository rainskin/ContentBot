from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, bot, list_of_channels
from states import States
from utils.check_admin_rights import is_admin


@dp.message_handler(state=States.get_channels_for_ad)
async def _(msg: types.Message, state: FSMContext):
    if not msg.entities:
        await msg.answer('Отправь сообщение, содержащее ссылки на канал')
        return

    channel_links = []

    for entity in msg.entities:
        link = entity['url'] or msg.text[entity.offset:entity.offset + entity.length]
        channel_links.append(link)

    channels = []
    channel_ids = []

    for link in channel_links:
        channel = list_of_channels.find_one({'link': link})
        if not channel:
            continue

        title = channel['title']
        _id = channel['id']
        channel_ids.append(_id)
        channels.append(title)

    if not channels:
        await msg.answer('Ты не выбрал каналы')
        return

    channel_text = "\n".join(channels)
    text = f'ты выбрал вот эти каналы:\n\n<b>{channel_text}</b>\n\nВсе верно?'
    await msg.answer(text, parse_mode='html', reply_markup=keyboards.YesOrNo())

    await state.update_data(channel_ids=channel_ids)
    await States.check_channels.set()
