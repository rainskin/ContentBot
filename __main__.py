import os

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import config
import texts
from src import loader, keyboards, image
from src.chromedriver.class_parser import Parser

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
COMMANDS = [
    types.BotCommand('start', 'Начать'),
    types.BotCommand('setup', 'Установка'),
    types.BotCommand('pars', 'Начать парсинг'),
    types.BotCommand('show', 'Посмотреть фотки'),
    types.BotCommand('test', 'тестиров_Очка'),
]


class States(StatesGroup):
    choosing_category = State()
    choosing_amount = State()


@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    # if message.from_user.id not in config.ADMIN_ID:
    #     return
    await state.finish()
    await message.answer(texts.cmd_start_text)
    await dp.bot.set_my_commands(COMMANDS)


@dp.message_handler(commands=["setup"])
async def cmd_setup(message: types.Message):
    if os.path.exists('cookies'):
        await message.answer('Авторизация уже пройдена, файл cookies найден')
    else:
        await message.answer('Прохожу авторизацию')
        Parser(config.path, config.username, config.password).authorization()
        await bot.send_message(message.chat.id, 'Готово')


@dp.message_handler(commands=["pars"])
async def cmd_pars(message: types.Message):
    if os.path.exists('cookies'):
        await bot.send_message(message.chat.id, 'Начинаю парсить')
        links = Parser(config.path, config.username, config.password).get_images(config.url)

        await bot.send_message(message.chat.id, 'Закончил')
        await bot.send_message(message.chat.id, 'Добавляю в дб')
        links_amount = []

        for url in links:
            item = {
                'url': url
            }
            if image.is_new(url) is True:
                loader.ecchi_col.insert_one(item)
                links_amount.append(item)

        await bot.send_message(message.chat.id, f'Количество новых пикч: {len(links_amount)}')
    else:
        await bot.send_message(message.chat.id, 'Сначала нужно пройти авторизацию. Жми /setup')


@dp.message_handler(commands=["show"])
async def cmd_show(message: types.Message):
    await message.answer('Выбери категорию', reply_markup=keyboards.category_kb)
    await States.choosing_category.set()


@dp.message_handler(state=States.choosing_category)
async def send_photo(message: types.Message, state: FSMContext):
    category = (message.text)
    await state.update_data(category=category, list=[])
    if category == 'Лайт':
        amount = loader.ecchi_col.count_documents({})
    else:
        amount = loader.hentai_coll.count_documents({})

    await message.answer(f'В этой категории {amount} изображений\nСколько пикч отправить?', )
    await States.choosing_amount.set()


@dp.message_handler(state=States.choosing_amount)
async def send_photo(message: types.Message, state: FSMContext):
    amount = int(message.text)

    data = await state.get_data()

    if data['list'] is None:
        image_list = []
    else:
        image_list = data['list']

    if data['category'] == "Лайт":
        value = loader.ecchi_col.count_documents({})
        for img in loader.ecchi_col.find(limit=amount + len(image_list)):
            img = img['url']
            if img not in image_list:
                image_list.append(img)
                await bot.send_photo(message.chat.id, photo=img, caption=img, reply_markup=keyboards.photo_kb)
    else:
        value = loader.hentai_coll.count_documents({})
        for img in loader.hentai_coll.find(limit=amount + len(image_list)):
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


@dp.message_handler()
async def help(message: types.Message):
    await bot.send_message(message.chat.id, texts.commands)


@dp.message_handler(commands=["test"])
async def cmd_test(message: types.Message):
    await message.answer('Тестируемся')
    photo = 'https://preview.redd.it/0ju4n3ksqd3a1.png?width=640&crop=smart&auto=webp&s=069777ae65849d2a1cefd4bc6b5e9529a3cb4a9c'
    msg = await bot.send_photo(message.chat.id, photo=photo, reply_markup=keyboards.test_kb)
    print(msg)
    print(msg.photo[-1].file_id)


@dp.callback_query_handler(text='test_btn')
async def delete_photo(callback_query: types.CallbackQuery):
    text = callback_query.message.photo[-1].file_id
    await bot.send_message(callback_query.message.chat.id, text)


@dp.callback_query_handler(text='delete_photo', state='*')
async def delete_photo(query: types.CallbackQuery):
    url = query.message.caption
    if loader.hentai_coll.find_one({'url': url}) is None:
        loader.ecchi_col.delete_one({'url': url})
    else:
        loader.hentai_coll.delete_one({'url': url})

    loader.blacklist.insert_one({'url': url})
    await query.message.delete()


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


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
