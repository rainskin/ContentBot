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

    for link in channel_links:
        channel = list_of_channels.find_one({'link': link})
        if not channel:
            continue

        title = channel['title']
        _id = channel['id']
        channel_ids.append(_id)
        channels.append(title)

    if channels:
        channels_in_text = "\n".join(links.add_links_to_titles(channels, channel_links))
        text = f'Выбраны следующие каналы:\n\n{channels_in_text}\n\nВсе верно?'
        await msg.answer(text, parse_mode='html', reply_markup=keyboards.YesOrNo(), disable_web_page_preview=True)
    elif channel_links:
        await msg.answer('Не нашел этих каналов в базе, проверь ссылки')
        return
    else:
        await msg.answer('Отправь сообщение, содержащее ссылки на канал')
        return

    await States.check_channels.set()
    await msg.delete()
    await state.update_data(channels=channels, channel_ids=channel_ids, channel_links=channel_links)



