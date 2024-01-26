import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions

import keyboards
from loader import ecchi_col, hentai_coll, dp, bot
from states import States


@dp.message_handler(state=States.choosing_amount)
async def send_photo(message: types.Message, state: FSMContext):
    amount = int(message.text)
    collection = ecchi_col
    data = await state.get_data()
    image_list = data.get('list', [])
    reply_markup = keyboards.photo_kb

    if data['category'] == "Лайт":
        value = ecchi_col.count_documents({})

    else:
        collection = hentai_coll
        value = collection.count_documents({})
        reply_markup = keyboards.delete_kb

    for img in collection.find(limit=amount + len(image_list)):
        img = img['url']
        if img not in image_list:
            image_list.append(img)
            await bot.send_photo(message.chat.id, photo=img, caption=img, reply_markup=reply_markup)
            await asyncio.sleep(0.1)

    await bot.send_message(message.chat.id,
                           f'В категории осталось {value - len(image_list)} картинок. Отправить еще? Введи количество')
    await state.update_data(list=image_list)

    if value - len(image_list) == 0:
        await bot.send_message(message.chat.id, 'Картинки закончились')
        await state.finish()


@dp.errors_handler(exception=exceptions.RetryAfter)
async def exception_handler(update: types.Update, exception: exceptions.RetryAfter):
    await asyncio.sleep(0.3)
    # await update.message.answer('Флуд контроль')
