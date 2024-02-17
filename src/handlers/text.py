from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
import texts
from config import SALE_GROUP_ID
from loader import dp, bot, list_of_channels
from states import States
from utils import links
from utils.check_admin_rights import is_admin


@dp.message_handler(content_types='any')
async def send_help(msg: types.Message, state: FSMContext):

    if msg.chat.id != SALE_GROUP_ID:
        return

    entities = msg.entities or msg.caption_entities

    if not entities:
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
    else:
        await msg.answer('Не нашел этих каналов в базе, проверь ссылки')
        return

    await States.check_channels.set()
    await msg.delete()
    await state.update_data(channels=channels, channel_ids=channel_ids, channel_links=channel_links)


