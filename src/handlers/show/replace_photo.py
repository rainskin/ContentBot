from aiogram import types

import loader
from loader import dp


@dp.callback_query_handler(text='replace_photo', state='*')
async def replace_photo(query: types.CallbackQuery):
    url = query.message.caption

    if loader.hentai_coll.find_one({'url': url}) is None:
        loader.hentai_coll.insert_one({'url': url})
        loader.ecchi_col.delete_one({'url': url})

        await query.answer("Переместил в хентай коллекцию", show_alert=True)
    else:
        loader.ecchi_col.delete_one({'url': url})
        await query.answer("Дубль, удалил", show_alert=True)

    await query.message.delete()
