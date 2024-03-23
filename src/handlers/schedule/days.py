from datetime import datetime
from utils.time import get_number_of_days_in_a_month, create_valid_date, RU_MONTHS_GEN, get_current_datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, bot
from states import States


@dp.message_handler(state=States.choosing_days)
async def schedule(message: types.Message, state: FSMContext):
    current_datetime = get_current_datetime()
    current_day = current_datetime['day']
    current_month = current_datetime['month']
    current_year = current_datetime['year']

    try:
        period = message.text.split()
        first_day = int(period[0])
        last_day = int(period[1])

    except (ValueError, IndexError):
        await bot.send_message(message.chat.id, 'Введи две даты через пробел')
        return

    first_date = create_valid_date(first_day, current_day, current_month, current_year)
    second_date = create_valid_date(last_day, current_day, current_month, current_year)

    if first_date.date() < datetime.now().date():
        await bot.send_message(message.chat.id, 'Нельзя запланировать на прошедшую дату')
        return

    number_of_days_in_a_month = get_number_of_days_in_a_month(current_year, current_month)
    if last_day > number_of_days_in_a_month:
        await bot.send_message(message.chat.id,
                               f'Нельзя запланировать на {last_day} число.\n\nВ текущем месяце {number_of_days_in_a_month} дней')
        return

    days = [first_day, last_day]

    first_date_str = str(first_date.day) + ' ' + RU_MONTHS_GEN[first_date.month - 1]
    second_date_str = str(second_date.day) + ' ' + RU_MONTHS_GEN[second_date.month - 1]

    if first_day != last_day:
        await bot.send_message(message.chat.id, F'Выбраны даты с <b>{first_date_str}</b> по <b>{second_date_str}</b>',
                               parse_mode='html')

    else:
        await bot.send_message(message.chat.id, F'Выбрана дата: {first_date_str}')
        days = [first_day]

    await state.update_data(days=days)
    await bot.send_message(message.chat.id, 'Теперь выбери время', reply_markup=keyboards.choose_time_kb)
    await States.choosing_time.set()


# def get_current_datetime():
#     c_datetime = datetime.now()
#
#     return {
#         'hour': c_datetime.hour,
#         'day': c_datetime.day,
#         'month': c_datetime.month,
#         'year': c_datetime.year,
#         'time': str(c_datetime.minute) + ':' + str(c_datetime.second)
#     }


