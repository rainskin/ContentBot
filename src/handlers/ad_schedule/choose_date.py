from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, bot, list_of_channels
from states import States
from utils.time import create_valid_date, RU_MONTHS_GEN

@dp.message_handler(state=States.choose_ad_date)
async def _(msg: types.Message, state: FSMContext):

    try:
        date = msg.text.split()
        day = int(date[0])
        hour = int(date[1])
        minutes = int(date[2])

    except (ValueError, IndexError):
        await bot.send_message(msg.chat.id, 'Введи две даты через пробел')
        return

    date = create_valid_date(day)
    month = RU_MONTHS_GEN[date.month]

    await States.schedule_ad.set()
    await state.update_data(hour=hour, minutes=minutes, day=day)
    await msg.answer(f'запланировать пост на <b>{day} {month}, {hour}:{minutes}</b>?', parse_mode='html', reply_markup=keyboards.YesOrNo())


