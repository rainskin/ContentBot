from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from config import SALE_GROUP_ID
from loader import dp, bot
from states import States
from utils import db
from utils.check_admin_rights import is_admin, is_saler

text = 'Отправь имя/юзернейм рекламодателя и цену через пробел\n\n Пример: <b>АДМИН 1000</b>'


@dp.callback_query_handler(text='add_sale_info', state=None)
async def _(query: types.CallbackQuery, state: FSMContext):
    if query.message.chat.id != SALE_GROUP_ID:
        return

    sale_msg_id = query.message.message_id
    if not is_admin(query.from_user.id) or not is_saler(query.from_user.first_name, sale_msg_id):
        await query.answer('У тебя нет прав для управления чужими продажами')
        return

    service_msg = await query.message.answer(text, parse_mode='html')
    await state.update_data(sale_msg_id=sale_msg_id, service_msg_id=service_msg.message_id)
    await States.add_sale_info.set()
    await query.answer()


@dp.callback_query_handler(text='update_sale_info', state=None)
async def _(query: types.CallbackQuery, state: FSMContext):
    if query.message.chat.id != SALE_GROUP_ID:
        return

    sale_msg_id = query.message.message_id

    if not is_admin(query.from_user.id) or not is_saler(query.from_user.first_name, sale_msg_id):
        await query.answer('У тебя нет прав для управления чужими продажами')
        return

    service_msg = await query.message.answer(text, parse_mode='html')
    await state.update_data(sale_msg_id=sale_msg_id, service_msg_id=service_msg.message_id)
    await States.add_sale_info.set()
    await query.answer()


@dp.message_handler(state=States.add_sale_info)
async def _(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    sale_msg_id = data['sale_msg_id']
    service_msg_id = data['service_msg_id']
    sale_msg_text = f'{await db.get_sale_msg_text(sale_msg_id)}\n\nplaceForAdInfo'

    try:
        sale_info = msg.text.split(' ')
        customer = sale_info[0]
        price = int(sale_info[1])
        sale_info_text = f'———————————————\n{customer} — <b>{str(price)} руб.</b>'

    except Exception as e:
        await msg.answer('Что-то пошло не так, попробуй еще раз')
        return

    await db.add_customer_info(sale_msg_id, customer, int(price), sale_info_text)
    new_sale_msg_text = sale_msg_text.replace('placeForAdInfo', f'{sale_info_text}')
    await bot.edit_message_text(new_sale_msg_text, msg.chat.id, sale_msg_id, parse_mode='html', disable_web_page_preview=True)
    await bot.delete_message(msg.chat.id, service_msg_id)
    await msg.delete()
    await bot.edit_message_reply_markup(msg.chat.id, sale_msg_id, reply_markup=keyboards.SaleSettings(sale_info=True,
                                                                                                      ad_is_scheduled=await db.scheduled_posts_is_exist(
                                                                                                          sale_msg_id)))
    await state.finish()


@dp.callback_query_handler(text='delete_sale', state=None)
async def _(query: types.CallbackQuery):
    if query.message.chat.id != SALE_GROUP_ID:
        return

    chat_id = query.message.chat.id
    sale_msg_id = query.message.message_id

    if not is_admin(query.from_user.id) or not is_saler(query.from_user.first_name, sale_msg_id):
        await query.answer('У тебя нет прав для удаления чужих продаж')
        return

    await db.delete_sale(sale_msg_id)
    await query.answer('Продажа удалена')
    await bot.delete_message(chat_id, sale_msg_id)

