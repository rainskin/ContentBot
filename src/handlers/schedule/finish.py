from aiogram import types
from aiogram.dispatcher import FSMContext

import config
from loader import dp, bot
from loader import ecchi_col, yuri, cute_pics, userbot
from states import States


@dp.callback_query_handler(state=States.accept)
async def finish(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.message.chat.id, 'Начинаю планирование постов')
    data = await state.get_data()
    chat = data['chat']
    chat_id = data['chat_id']
    days = data['days']
    time = data['time']
    collection = ''
    search_parameter = 'id'
    caption = ''
    blacklist = False
    print(days)
    print(time)
    if chat == 'anime_tyan':
        collection = ecchi_col
        search_parameter = 'url'
        blacklist = True
        caption = '__Channel:__ **[@anime4_tyan](https://t.me/+H2QjcBkVtcs4ZDNi)**'
    elif chat == 'yuri':
        collection = yuri
        caption = '🎀 **[Yuri arts](https://t.me/+NTDsUr6Stvs3OWZi)**'

    elif chat == 'cute_pics':
        collection = cute_pics

    total_photos_count = collection.count_documents({})
    requested_photos_count = len(days) * len(time)
    print(total_photos_count)

    if requested_photos_count > total_photos_count:
        await bot.send_message(callback_query.message.chat.id,
                               f'В коллекции *{total_photos_count}* ты запросил {requested_photos_count}\nПополни '
                               f'коллекцию, либо выбери другие даты',
                               parse_mode=types.ParseMode.MARKDOWN)
    else:
        await userbot.schedule(chat_id, collection, days, time, search_parameter, caption, blacklist=blacklist)
        await bot.send_message(callback_query.message.chat.id, 'Готово')
        await state.finish()
