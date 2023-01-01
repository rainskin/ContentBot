from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import ecchi_col, hentai_coll, dp
from states import States


@dp.message_handler(state=States.choosing_category)
async def send_photo(message: types.Message, state: FSMContext):
    category = message.text
    await state.update_data(category=category, list=[])

    if category == 'Лайт':
        amount = ecchi_col.count_documents({})

    elif category == 'Хентай':
        amount = hentai_coll.count_documents({})

    else:
        await message.answer('Выбери категорию')
        return


    await message.answer(f'В этой категории {amount} изображений\nСколько пикч отправить?')
    await States.choosing_amount.set()
