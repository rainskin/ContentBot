from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, bot, list_of_channels
from states import States
from utils.check_admin_rights import is_admin


@dp.message_handler(state=States.waiting_ad_post, content_types="any")
async def _(msg: types.Message, state: FSMContext):
    msg_text = msg.caption or msg.text
    title = msg_text[0:40] if msg_text else 'Вложение'

    data = await state.get_data()
    message_ids = data.get('message_ids', [])

    if msg.media_group_id is not None:
        # data = await state.get_data()
        group_id_in_data = data.get('group_id')

        if group_id_in_data == msg.media_group_id:
            pass

        else:
            group_id = msg.media_group_id

            await state.update_data(group_id=group_id)
            new_message_id = msg.message_id
            await state.update_data(message_id=message_ids + [new_message_id])
            await msg.answer(f'Пост (альбом) <b>"{title}..."</b> принят', parse_mode='html')
            await msg.answer('Теперь в веди дату и в время через пробел в формате <b>ДАТА ЧАСЫ МИНУТЫ</b>',
                             parse_mode='html')

    else:

        new_message_id = msg.message_id
        message_id = data.get('message_ids')
        await state.update_data(message_id=message_ids + [new_message_id])
        await msg.answer(f'Пост <b>"{title}..."</b> принят', parse_mode='html')
        await msg.answer('Теперь в веди дату и в время через пробел в формате <b>ДАТА ЧАСЫ МИНУТЫ</b>',
                         parse_mode='html')


    await States.choose_ad_date.set()


content_types = ["text", "sticker", "voice", "photo", "poll", "video_note"]
