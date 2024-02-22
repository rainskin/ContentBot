from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp
from states import States


# @dp.callback_query_handler(text='yes', state=States.check_channels)
# async def add_admin(query: types.CallbackQuery, state: FSMContext):
#     await query.message.edit_reply_markup(None)
#     await query.message.answer('Отправь пост')
#     await States.waiting_ad_post.set()

@dp.callback_query_handler(text='yes', state=States.check_channels)
async def add_admin(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(None)
    msg_ask_to_select_data = await query.message.answer('Отправь дату (только число)', reply_markup=keyboards.AdDate())
    await state.update_data(msg_ask_to_select_data_id=msg_ask_to_select_data.message_id)
    await query.message.delete()
    await States.choose_ad_date.set()



@dp.callback_query_handler(text='no', state=States.check_channels)
async def add_admin(query: types.CallbackQuery, state: FSMContext):
    await query.answer('Действие отменено')
    await state.finish()
    await query.message.delete()

