from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import ecchi_col, hentai_coll, dp, bot
from states import States


@dp.message_handler(state=States.choosing_amount)
async def send_photo(message: types.Message, state: FSMContext):
    amount = int(message.text)

    data = await state.get_data()

    if data['list'] is None:
        image_list = []
    else:
        image_list = data['list']

    if data['category'] == "Лайт":
        value = ecchi_col.count_documents({})
        for img in ecchi_col.find(limit=amount + len(image_list)):
            img = img['url']
            if img not in image_list:
                image_list.append(img)
                await bot.send_photo(message.chat.id, photo=img, caption=img, reply_markup=keyboards.photo_kb)
    else:
        value = hentai_coll.count_documents({})
        for img in hentai_coll.find(limit=amount + len(image_list)):
            img = img['url']
            if img not in image_list:
                image_list.append(img)
                await bot.send_photo(message.chat.id, photo=img, caption=img, reply_markup=keyboards.delete_kb)

    await bot.send_message(message.chat.id,
                           f'В категории осталось {value - len(image_list)} картинок. Отправить еще? Введи количество')
    await state.update_data(list=image_list)

    if value - len(image_list) == 0:
        await bot.send_message(message.chat.id, 'Картинки закончились')
        await state.finish()
