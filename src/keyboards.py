from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

delete_btn = InlineKeyboardButton('Удалить', callback_data='delete_photo')
replace_btn = InlineKeyboardButton('Переместить в 🔞', callback_data='replace_photo')
photo_kb = InlineKeyboardMarkup().add(delete_btn, replace_btn)
delete_kb = InlineKeyboardMarkup().add(delete_btn)

test_btn = InlineKeyboardButton('ТЕСТ ЧИ ДА', callback_data='test_btn')
test_kb = InlineKeyboardMarkup().add(test_btn)

category_lite_btn = KeyboardButton('Лайт')
category_18_btn = KeyboardButton('Хентай')

category_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(category_lite_btn, category_18_btn)

remove = ReplyKeyboardRemove()

# Каналы
anime_tyan = InlineKeyboardButton('Аниме тянки', callback_data='anime_tyan')
yuri = InlineKeyboardButton('Юри', callback_data='yuri')
cute_pics = InlineKeyboardButton('Пикчи для диалогов', callback_data='cute_pics')
# Клавиатура с каналами
channels_kb = InlineKeyboardMarkup(row_width=1).add(anime_tyan, yuri, cute_pics)
