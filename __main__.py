import os

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode

import config
import texts
from src import loader, keyboards, image
from src.chromedriver.class_parser import Parser
from src.userbot import Userbot

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
userbot = Userbot()

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
    schedule = State()
    choosing_days = State()
    choosing_time = State()


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


@dp.message_handler(commands=["schedule"])
async def cmd_schedule(message: types.Message):
    await message.answer(text=texts.schedule_main, reply_markup=keyboards.channels_kb)
    await States.schedule.set()


@dp.callback_query_handler(state=States.schedule)
async def chose_category(callback_query: types.CallbackQuery, state: FSMContext):
    chat = callback_query.data
    channel_name = ''
    chat_id = ''
    if chat == 'anime_tyan':
        channel_name = 'Аниме тянки'
        chat_id = config.TYAN_ID

    elif chat == 'yuri':
        channel_name = 'Юри'
        chat_id = config.YURI_ID

    elif chat == 'cute_pics':
        channel_name = 'Пикчи для диалогов'
        chat_id = config.CUTE_PICS_ID

    await state.update_data({'chat': chat, 'chat_id': chat_id})
    await bot.send_message(callback_query.message.chat.id, f'Ты выбрал канал *{channel_name}*',
                           parse_mode=ParseMode.MARKDOWN)
    await bot.send_message(callback_query.message.chat.id, text=texts.choosing_days, parse_mode=ParseMode.MARKDOWN)
    await States.choosing_days.set()


@dp.message_handler(state=States.choosing_days)
async def schedule(message: types.Message, state: FSMContext):
    period = message.text.split(' ')
    first_day = int(period[0])
    last_day = int(period[1])
    days = list(range(first_day, last_day + 1))
    time = [10, 11, 13]
    data = await state.get_data()
    chat = data['chat']
    chat_id = data['chat_id']
    collection = ''
    if chat == 'anime_tyan':
        collection = loader.ecchi_col

    elif chat == 'yuri':
        collection = loader.yuri

    elif chat == 'cute_pics':
        collection = loader.cute_pics

    await userbot.schedule(config.TEST_CHANNEL_ID, collection, days, time)
    # print(s, type(s))



@dp.message_handler()
async def help(message: types.Message):
    await bot.send_message(message.chat.id, texts.commands)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
