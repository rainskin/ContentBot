from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import States
from utils.time import create_valid_date, RU_MONTHS_GEN, current_day, number_of_days_in_a_month


@dp.message_handler(state=States.choose_ad_date)
async def _(msg: types.Message, state: FSMContext):
    try:
        datetime = msg.text.split()
        day = int(datetime[0])

    except (ValueError, IndexError):
        await msg.answer('Дата указана неверно')
        await msg.delete()
        return

    if not is_correct_day(day):
        await msg.answer('В текущем месяце нет столько дней')
        await msg.delete()
        return

    text = await get_text_with_valid_date(state, day)
    await msg.answer(text, parse_mode='html')
    await msg.delete()


@dp.callback_query_handler(state=States.choose_ad_date)
async def _(query: types.CallbackQuery, state: FSMContext):
    text = query.data

    if text == 'today':
        day = current_day
    elif text == 'tomorrow':
        day = current_day + 1
    else:
        await query.answer('куда ты звонишь сынок')
        return

    text = await get_text_with_valid_date(state, day)
    msg_with_date = await query.message.answer(text, parse_mode='html')
    await query.answer()
    await query.message.delete()
    await state.update_data(msg_with_date_id=msg_with_date.message_id)


async def get_text_with_valid_date(state: FSMContext, day) -> str:

    date = create_valid_date(day)
    month = date.month
    month_name = RU_MONTHS_GEN[date.month - 1]
    year = date.year
    text = f'Выбрана дата <b>{day} {month_name}</b> \n\n Отправь время в формате: <b>19 05</b>'
    await States.choose_ad_time.set()
    await state.update_data(day=day, month=month, month_name=month_name, year=year)
    return text


def is_correct_day(day):
    return 0 < day < number_of_days_in_a_month
