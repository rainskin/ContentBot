from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, bot
from states import States


@dp.callback_query_handler(state=States.choosing_time)
async def choosing_time(query: types.CallbackQuery, state: FSMContext):
    data = query.data
    time = [int(i) for i in data.split(', ')]

    await state.update_data(time=time)
    await query.message.delete()
    await bot.send_message(query.message.chat.id, f'Ты выбрал следующие временные слоты:\n{time}',
                           reply_markup=keyboards.finish_schedule_kb)
    await States.accept.set()


