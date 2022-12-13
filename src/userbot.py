from _datetime import datetime
from random import randint

import pyrogram
from pyrogram import types, filters
from pyrogram.enums import ParseMode

import loader, config


app = pyrogram.Client('../userbot', config.API_ID, config.API_HASH)

chat = '-1001862978453'
time_5 = [10, 13, 16, 19, 22]
time_4 = [10, 14, 18, 22]
time_3 = [8, 14, 20]

caption_tyan = '__Channel:__ **[@anime4_tyan](https://t.me/+H2QjcBkVtcs4ZDNi)**'
caption_yuri = '🎀 **[Yuri arts](https://t.me/+NTDsUr6Stvs3OWZi)**'




@app.on_message(filters.chat(-1001862978453))
def add_picture(_, msg: types.Message):
    id = msg.photo.file_id
    item = {
        'id': id
    }
    loader.avatars.insert_one(item)
    # app.send_photo(chat_id=config.TEST_CHANNEL_ID, photo=a)


def schedule():
    app.start()
    # Для соло пикч
    for a in [13, 14, 15, 16, 17, 18, 19]:  # Дни
        for i in time_3:  # Время
            data = datetime(year=datetime.now().year, month=datetime.now().month, day=a, hour=i,
                            minute=randint(0, 10))
            img = loader.avatars.find_one()['id']
            loader.avatars.delete_one({'id': img})
            print(img)

            app.send_photo(chat_id=config.AVATARS_ID, parse_mode=ParseMode.MARKDOWN, photo=img,
                           schedule_date=data)


def forward(days, hours):
    my_date = {}
    id = 0
    for i in days:
        a = {
            'day': i,
            'hour': hours
        }
        id += 1
        my_date[id] = a
        # my_date['day'] = i
        # my_date['hour'] = hours
        print(a)

    # data = datetime(year=datetime.now().year, month=datetime.now().month, day=a, hour=i,
    #                 minute=randint(0, 10))

    print(my_date)
    print(len(my_date))


days = [25, 26]
hours = [10, 12, 13]
# app.run()
forward(days, hours)
# schedule()
