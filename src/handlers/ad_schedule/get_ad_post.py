import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup

import config
import keyboards
from loader import dp, userbot, bot
from states import States
from utils import links
from utils.msg_marker import get_marker


@dp.message_handler(state=States.waiting_ad_post, content_types="any")
async def _(msg: types.Message, state: FSMContext):
    msg_text = msg.caption or msg.text
    title = msg_text[0:40] if msg_text else 'Вложение'
    title = title.replace("<", " ")

    data = await state.get_data()
    service_msg_id = data.get('service_msg_id')
    notification = True
    drop_author = False
    inline_keyboard = False

    if msg.media_group_id:
        group_id_in_data = data.get('group_id')
        message_ids = data.get('message_id', [])
        message_markers = data.get('message_markers', [])
        marker = get_marker(msg)
        if group_id_in_data == msg.media_group_id:
            await state.update_data(message_markers=message_markers + [marker])
            return

        group_id = msg.media_group_id
        await state.update_data(group_id=group_id)
        new_msg_id = msg.message_id
        await state.update_data(message_id=message_ids + [new_msg_id], message_markers=message_markers + [marker],
                                is_album=True)
        await asyncio.sleep(2)
        ad_title_text = f'Пост (альбом) <b>"{title}..."</b> принят'
        ad_title_msg = await msg.answer(ad_title_text,
                                        reply_markup=keyboards.AdPostSettings(drop_author=drop_author,
                                                                              notification=notification),
                                        parse_mode='html', disable_web_page_preview=True)

    else:
        marker = get_marker(msg)
        await state.update_data(message_id=msg.message_id, message_markers=[marker], is_album=False)
        ad_title_text = f'Пост <b>"{title}..."</b> принят'
        await asyncio.sleep(2)

        ad_title_msg = await msg.answer(ad_title_text, parse_mode='html',
                                        reply_markup=keyboards.AdPostSettings(drop_author=drop_author,
                                                                              notification=notification,
                                                                              inline_keyboard=bool(msg.reply_markup)),
                                        disable_web_page_preview=True)
    if msg.reply_markup:
        keyboard_data = (parse_keyboard(msg.reply_markup))
    else:
        keyboard_data = None

    link = await links.get_links_from_msg(msg)

    await state.update_data(from_chat_id=msg.chat.id, drop_author=drop_author, notification=notification,
                            inline_keyboard=inline_keyboard, link=link, title=title,
                            ad_title_msg_id=ad_title_msg.message_id,
                            ad_title_text=ad_title_text, keyboard_data=keyboard_data)
    await bot.delete_message(msg.chat.id, service_msg_id)
    await States.schedule_ad.set()


ф = {"inline_keyboard": [[{"text": "Сатору", "url": "https://t.me/+2ExCEP4sUug3NDQy"},
                          {"text": "Нобара", "url": "https://t.me/+gdVGQUO-ZblmMWMy"}],
                         [{"text": "Незуко", "url": "https://t.me/+PgyPdt8UUls3NjUy"},
                          {"text": "Иноске", "url": "https://t.me/+gTMUcy47Bv4yMTc6"}],
                         [{"text": "Синобу", "url": "https://t.me/+ZExxEnsEoxJhOGNi"},
                          {"text": "Дзэницу", "url": "https://t.me/+YEnnhIvEnj84ZjEy"}],
                         [{"text": "Мао Мао", "url": "https://t.me/+_AImv1y3BtwyOTli"},
                          {"text": "Жэньши", "url": "https://t.me/+ap-HAZrZrhkwNmJi"}],
                         [{"text": "Дазай", "url": "https://t.me/+MEWJIkltJ-BiODRi"},
                          {"text": "Достоевский", "url": "https://t.me/+8xyDn6aNp3g1MDMy"}],
                         [{"text": "Макима", "url": "https://t.me/+pF2t_6Bvx-43NGNi"},
                          {"text": "Дэндзи", "url": "https://t.me/+EysAjgUyr5FjNmEy"}],
                         [{"text": "Киллуа", "url": "https://t.me/+F564fiHe3cdkNmM6"},
                          {"text": "Хисока", "url": "https://t.me/+cWa8wTFq1xgxNGQy"}],
                         [{"text": "Джотаро", "url": "https://t.me/+2Icz5VDzNihlYTBi"},
                          {"text": "Спидвагон", "url": "https://t.me/+xO4Qyu68DzM3MWFi"}],
                         [{"text": "Джорно", "url": "https://t.me/+GyQbXR1TDMZmMzgy"},
                          {"text": "Хошино Ай", "url": "https://t.me/+wCBNJUlQqvBhOWQy"}],
                         [{"text": "Рюк", "url": "https://t.me/+G18VQq8LlHQ5ZWYy"},
                          {"text": "Йоичи Исаги", "url": "https://t.me/+LWenljI1x7gyNWRi"}],
                         [{"text": "Танджиро", "url": "https://t.me/+4X0uso21fu9mYzhi"},
                          {"text": "Изуку", "url": "https://t.me/+PegvEYjNE7BhNzky"}],
                         [{"text": "Йора Форджер", "url": "https://t.me/+kBWLxAyrzcc5YzYy"},
                          {"text": "Итадори", "url": "https://t.me/+xjlP9CZz3zkwMjEy"}]]}

b = {"inline_keyboard": [[{"text": "Рисуем эмоции", "url": "https://t.me/+hom-9Dr2lQoyMDAy"}],
                         [{"text": "Рисуем пошлое", "url": "https://t.me/+iN1kyRMgEfMzMjZi"}],
                         [{"text": "Рисуем фигуры", "url": "https://t.me/+cNFACymJRz81MWFi"}]]}


def parse_keyboard(keyboard: InlineKeyboardMarkup):
    data = keyboard.to_python().get('inline_keyboard')

    text_data = ''
    for row in data:
        row_data = ''
        for button in row:
            button_data = f"{button['text']} - {button['url']}"
            if row_data:
                sep = ' | '
                row_data += f'{sep}{button_data}'
            else:
                row_data += button_data
        if text_data:
            sep = '\n'
            text_data += f'{sep}{row_data}'
        else:
            text_data += row_data

    return text_data
# кнопка 1 - ссылка
# кнопка 2 - ссылка | кнопка 3 - ссылка

# ряд разделяется по переносу строки, кнопки  в ряду по знаку |
