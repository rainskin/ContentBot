from _datetime import datetime
from random import randint

import pyrogram
from pyrogram.enums import ParseMode

import config
import loader


# name: str, api_id: Union[int, str] = None, api_hash: str = None
class Userbot:

    def __init__(self):
        self.app = pyrogram.Client('../userbot', config.API_ID, config.API_HASH)

    async def schedule(self, chat_id, collection, days: list, time_slots: list, search_parameter, caption, blacklist: bool):
        app = self.app
        try:
            await app.start()
        except ConnectionError:
            print('Уже подключен')
        # Для соло пикч
        search_parameter = search_parameter
        for day in days:  # Дни (список)
            for time in time_slots:  # Время
                data = datetime(year=datetime.now().year, month=datetime.now().month, day=day, hour=time,
                                minute=randint(0, 10))
                img = collection.find_one()[search_parameter]

                if blacklist == True:
                    loader.blacklist.insert_one({'url': img})
                collection.delete_one({search_parameter: img})

                await app.send_photo(chat_id=chat_id, caption=caption, parse_mode=ParseMode.MARKDOWN, photo=img,
                                     schedule_date=data)

# app = pyrogram.Client('../userbot', config.API_ID, config.API_HASH)

# chat = '-1001862978453'
# time_5 = [10, 13, 16, 19, 22]
# time_4 = [10, 14, 18, 22]
# time_3 = [8, 14, 20]
# days = list(range(20, 27))

# @app.on_message(filters.chat(-1001862978453))
# def add_picture(_, msg: types.Message):
#     id = msg.photo.file_id
#     item = {
#         'id': id
#     }
#     loader.cute_pics.insert_one(item)
#     # app.send_photo(chat_id=config.TEST_CHANNEL_ID, photo=id)


# def schedule():
#     app.start()
#     # Для соло пикч
#     for a in days:  # Дни (список)
#         for i in time_3:  # Время
#             data = datetime(year=datetime.now().year, month=datetime.now().month, day=a, hour=i,
#                             minute=randint(0, 10))
#             img = loader.cute_pics.find_one()['id']
#             # loader.blacklist.insert_one({'url': img})
#             loader.cute_pics.delete_one({'id': img})
#             print(img)
#
#             app.send_photo(chat_id=config.TEST_CHANNEL_ID, parse_mode=ParseMode.MARKDOWN, photo=img,
#                            schedule_date=data)


# def forward(days, hours):
#     my_date = {}
#     id = 0
#     for i in days:
#         a = {
#             'day': i,
#             'hour': hours
#         }
#         id += 1
#         my_date[id] = a
#         # my_date['day'] = i
#         # my_date['hour'] = hours
#         print(a)
#
#     # data = datetime(year=datetime.now().year, month=datetime.now().month, day=a, hour=i,
#     #                 minute=randint(0, 10))
#
#     print(my_date)
#     print(len(my_date))


#
# # days = [25, 26]
# hours = [10, 12, 13]
# app.run()
# forward(days, hours)
# schedule()
