from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, list_of_admins, bot
from states import States
from utils.check_admin_rights import is_admin


@dp.callback_query_handler(text='yes', state=States.check_channels)
async def add_admin(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(None)
    await query.message.answer('Отправь пост')
    await States.waiting_ad_post.set()

@dp.callback_query_handler(text='no', state=States.check_channels)
async def add_admin(query: types.CallbackQuery, state: FSMContext):
    await query.answer('Действие отменено')
    await state.finish()
    await query.message.delete()

