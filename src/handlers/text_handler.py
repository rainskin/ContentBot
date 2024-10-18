
from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from core import db
from core.db import users
from loader import dp, bot, list_of_channels
from states import States
from utils import links



@dp.message_handler(content_types='any')
async def _(msg: types.Message, state: FSMContext):
    channel_owner_id = msg.from_user.id
    sale_group_id = await users.get_sale_group_id(channel_owner_id)

    if not sale_group_id:
        return

    if msg.chat.id != sale_group_id:
        return

    entities = msg.entities or msg.caption_entities

    if not entities:
        return

    user_id = msg.from_user.id
    channel_owner_id = user_id
    channel_links = await links.get_links_from_msg(msg)

    channels = []
    channel_ids = []

    user_channels = await db.channels.get_channels(user_id)
    for link in channel_links:
        for user_channel in user_channels:
            channel_link = user_channel.get('link')
            # channel = list_of_channels.find_one({'link': link})
            if link != channel_link:
                continue

            title = user_channel['title']
            _id = user_channel['id']
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
        return

    await States.check_channels.set()
    await msg.delete()
    await state.update_data(channel_owner_id=channel_owner_id, channels=channels, channel_ids=channel_ids, channel_links=channel_links)



