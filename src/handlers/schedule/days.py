from datetime import datetime
from calendar import monthrange
from utils.time import current_day, number_of_days_in_a_month, create_valid_date, RU_MONTHS_GEN

from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, bot
from states import States


@dp.message_handler(state=States.choosing_days)
async def schedule(message: types.Message, state: FSMContext):
    try:
        period = message.text.split()
        first_day = int(period[0])
        last_day = int(period[1])

    except (ValueError, IndexError):
        await bot.send_message(message.chat.id, 'Введи две даты через пробел')
        return

    if first_day < current_day:
        await bot.send_message(message.chat.id, 'Нельзя запланировать на прошедшую дату')
        return

    if last_day > number_of_days_in_a_month:
        await bot.send_message(message.chat.id,
                               f'Нельзя запланировать на {last_day} число.\n\nВ текущем месяце {number_of_days_in_a_month} дней')
        return

    days = [first_day, last_day]

    first_date = create_valid_date(first_day)
    second_date = create_valid_date(last_day)

    first_date_str = str(first_date.day) + ' ' + RU_MONTHS_GEN[first_date.month]
    second_date_str = str(second_date.day) + ' ' + RU_MONTHS_GEN[second_date.month]

    if first_day != last_day:
        await bot.send_message(message.chat.id, F'Выбраны даты с <b>{first_date_str}</b> по <b>{second_date_str}</b>', parse_mode='html')

    else:
        await bot.send_message(message.chat.id, F'Выбрана дата: {first_date_str}')
        days = [first_day]

    await state.update_data(days=days)
    await bot.send_message(message.chat.id, 'Теперь выбери время', reply_markup=keyboards.choose_time_kb)
    await States.choosing_time.set()
