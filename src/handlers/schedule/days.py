from datetime import datetime
from calendar import monthrange

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

    current_day = datetime.today().day
    current_year = datetime.now().year
    current_month = datetime.now().month

    number_of_days_in_a_month = monthrange(current_year, current_month)[1]

    if first_day < current_day:
        await bot.send_message(message.chat.id, 'Нельзя запланировать на прошедшую дату')
    elif last_day > number_of_days_in_a_month:
        await bot.send_message(message.chat.id, f'Нельзя запланировать на {last_day} число.\n\nВ текущем месяце {number_of_days_in_a_month} дней')
    else:
        days = list(range(first_day, last_day + 1))

        if first_day != last_day:
            await bot.send_message(message.chat.id, F'Выбраны даты с {first_day} по {last_day}')

        else:
            await bot.send_message(message.chat.id, F'Выбрана дата: {first_day} число')
            days = [first_day]

        await state.update_data(days=days)
        await bot.send_message(message.chat.id,'Теперь выбери время', reply_markup=keyboards.choose_time_kb)
        await States.choosing_time.set()
