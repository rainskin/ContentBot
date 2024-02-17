from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from utils.links import add_links_to_titles
from loader import dp, bot
from states import States
from utils.db import add_sale
from utils.time import is_not_correct_time


@dp.message_handler(state=States.choose_ad_time)
async def _(msg: types.Message, state: FSMContext):
    time = msg.text

    if len(time) <= 2:
        try:
            hour = int(time)
            minutes = 0
        except ValueError:
            await msg.answer('Используй только цифры')
            await msg.delete()
            return

    elif 4 <= len(time) <= 5:
        try:
            hour = int(time[:2])
            minutes = int(time[-2:])

        except ValueError:
            await msg.answer('Используй только цифры')
            await msg.delete()
            return

    else:
        await msg.answer('Неверный формат времени')
        await msg.delete()
        return

    if is_not_correct_time(hour, minutes):
        await msg.answer('Неверный формат времени')
        await msg.delete()
        return

    data = await state.get_data()

    str_minutes = str(minutes) if len(str(minutes)) == 2 else '0' + str(minutes)
    str_time = str(hour) + ':' + str_minutes

    #
    day = data['day']
    month = data['month']
    month_name = data['month_name']
    year = data['year']
    channels = data['channels']
    links = data['channel_links']
    channel_ids = data['channel_ids']
    msg_with_date_id = data['msg_with_date_id']

    channels_in_text = "\n".join(add_links_to_titles(channels, links))

    sale_date = f'📆 #{day}_{month_name}, {str_time}'
    salesman = f'(👤 {msg.from_user.first_name})'
    sale_title = f'<b>Продажа</b>'
    text = f'{sale_date}\n\n{sale_title} {salesman}\n\n{channels_in_text}'

    sale_msg = await msg.answer(text, parse_mode='html', disable_web_page_preview=True, reply_markup=keyboards.SaleSettings())
    await state.update_data(hour=hour, minutes=minutes)

    await add_sale(
        salesman[3:-1],
        sale_msg.message_id,
        [day, month, year],
        str_time,
        channel_ids
    )
    await bot.delete_message(msg.chat.id, msg_with_date_id)
    await msg.delete()
    await state.finish()




