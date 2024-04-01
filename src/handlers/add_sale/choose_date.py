from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import States
from utils.time import create_valid_date, RU_MONTHS_GEN, get_number_of_days_in_a_month, one_day, get_current_datetime


@dp.message_handler(state=States.choose_ad_date)
async def _(msg: types.Message, state: FSMContext):
    try:
        date_time = msg.text.split()
        day = int(date_time[0])

    except (ValueError, IndexError):
        await msg.answer('Дата указана неверно')
        await msg.delete()
        return

    current_datetime = get_current_datetime()
    current_year = current_datetime['year']
    current_month = current_datetime['month']
    current_day = current_datetime['day']
    number_of_days_in_a_month = get_number_of_days_in_a_month(current_year, current_month)
    if not is_correct_day(day, number_of_days_in_a_month):
        await msg.answer('В текущем месяце нет столько дней')
        await msg.delete()
        return

    date = create_valid_date(day, current_day, current_month, current_year)
    text = await get_text_with_valid_date(state, date)
    msg_with_date = await msg.answer(text, parse_mode='html')
    await state.update_data(msg_with_date_id=msg_with_date.message_id)
    await msg.delete()


@dp.callback_query_handler(state=States.choose_ad_date)
async def _(query: types.CallbackQuery, state: FSMContext):
    text = query.data

    date = datetime.now()
    if text == 'today':
        date = date
    elif text == 'tomorrow':
        date = date + one_day
    elif text == 'yesterday':
        date = date - one_day

    msg_text = await get_text_with_valid_date(state, date)
    msg_with_date = await query.message.answer(msg_text, parse_mode='html')
    await query.answer()
    await state.update_data(msg_with_date_id=msg_with_date.message_id)


async def get_text_with_valid_date(state: FSMContext, date: datetime) -> str:
    day = date.day

    month = date.month
    year = date.year
    month_name = RU_MONTHS_GEN[date.month - 1]
    text = f'Выбрана дата <b>{day} {month_name}</b> \n\n Отправь время в формате: <b>19 05</b>'
    await States.choose_ad_time.set()
    await state.update_data(day=day, month=month, month_name=month_name, year=year)
    return text


def is_correct_day(day: int, number_of_days_in_a_month: int) -> bool:
    return 0 < day <= number_of_days_in_a_month
