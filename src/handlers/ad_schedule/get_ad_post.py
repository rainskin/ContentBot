from aiogram import types
from aiogram.dispatcher import FSMContext

import config
import keyboards
from loader import dp, userbot, bot
from states import States
from utils import links


@dp.message_handler(state=States.waiting_ad_post, content_types="any")
async def _(msg: types.Message, state: FSMContext):
    msg_text = msg.caption or msg.text
    title = msg_text[0:40] if msg_text else 'Вложение'

    data = await state.get_data()
    service_msg_id = data.get('service_msg_id')
    notification = True
    drop_author = False

    if msg.media_group_id:
        group_id_in_data = data.get('group_id')

        if group_id_in_data == msg.media_group_id:
            return

        group_id = msg.media_group_id

        await state.update_data(group_id=group_id)
        message_ids = await userbot.get_msg_ids(config.UPLOAD_CHANNEL_ID, msg.message_id)
        await state.update_data(message_id=message_ids)
        ad_title_text = f'Пост (альбом) <b>"{title}..."</b> принят'
        ad_title_msg = await msg.answer(ad_title_text,
                                        reply_markup=keyboards.AdPostSettings(drop_author=drop_author,
                                                                              notification=notification),
                                        parse_mode='html', disable_web_page_preview=True)

    else:

        await state.update_data(message_id=msg.message_id)
        ad_title_text = f'Пост <b>"{title}..."</b> принят'
        ad_title_msg = await msg.answer(ad_title_text, parse_mode='html',
                                        reply_markup=keyboards.AdPostSettings(drop_author=drop_author,
                                                                              notification=notification),
                                        disable_web_page_preview=True)

    link = await links.get_links_from_msg(msg)
    await state.update_data(drop_author=drop_author, notification=notification, link=link, title=title, ad_title_msg_id=ad_title_msg.message_id,
                            ad_title_text=ad_title_text)
    await bot.delete_message(msg.chat.id, service_msg_id)
    await States.schedule_ad.set()


@dp.callback_query_handler(state=States.schedule_ad)
async def toggle_notification(query: types.CallbackQuery, state: FSMContext):
    text = query.data

    data = await state.get_data()
    drop_author = data['drop_author']
    notification = data['notification']

    if text == 'toggle_notification':
        notification = not notification
    elif text == 'toggle_author':
        drop_author = not drop_author

    await state.update_data(drop_author=drop_author, notification=notification)
    await query.message.edit_reply_markup(keyboards.AdPostSettings(drop_author=drop_author, notification=notification))
    await query.answer()
