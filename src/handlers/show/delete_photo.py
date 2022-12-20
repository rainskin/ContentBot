from aiogram import types

import loader
from loader import dp


@dp.callback_query_handler(text='delete_photo', state='*')
async def delete_photo(query: types.CallbackQuery):
    url = query.message.caption
    if loader.hentai_coll.find_one({'url': url}) is None:
        loader.ecchi_col.delete_one({'url': url})
    else:
        loader.hentai_coll.delete_one({'url': url})

    loader.blacklist.insert_one({'url': url})
    await query.message.delete()
