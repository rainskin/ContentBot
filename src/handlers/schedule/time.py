from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, bot
from states import States


@dp.callback_query_handler(state=States.choosing_time)
async def choosing_time(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    time = []

    if data == 'time_2':
        time = [8, 20]
    if data == 'time_3':
        time = [8, 14, 20]
    elif data == 'time_4':
        time = [10, 14, 18, 20]
    elif data == 'time_5':
        time = [10, 13, 16, 19, 22]

    await state.update_data(time=time)
    await callback_query.message.delete()
    await bot.send_message(callback_query.message.chat.id, f'Ты выбрал следующие временные слоты:\n{time}',
                           reply_markup=keyboards.finish_schedule_kb)
    await States.accept.set()


