import pyrogram
from pyrogram.enums import ParseMode

import config
import loader


class Userbot:

    def __init__(self):
        self.app = pyrogram.Client('../userbot', config.API_ID, config.API_HASH)

    async def copy(self, chat_id, search_parameter, caption, date):
        app = self.app
        try:
            await app.start()
        except ConnectionError:
            pass
        search_parameter = search_parameter

        message = loader.other_channels.find_one({'channel': search_parameter})['msg_id']

        try:
            # Для альбомов
            await app.copy_media_group(chat_id=chat_id, from_chat_id=-1001723603976, message_id=message,
                                       captions=caption,
                                       schedule_date=date)
        except ValueError:
            # Для соло пикч
            await app.copy_message(chat_id=chat_id, from_chat_id=-1001723603976, message_id=message,
                                   caption=caption,
                                   schedule_date=date)

        loader.other_channels.delete_one({'msg_id': message})

    async def schedule(self, chat_id, search_parameter, caption, date, anime_tyan: bool):

        # Отложка для канала Аниме Тянки

        app = self.app

        try:
            await app.start()
        except ConnectionError:
            pass

        if anime_tyan:
            img = loader.ecchi_col.find_one()[search_parameter]
            loader.ecchi_col.delete_one({'url': img})
            loader.blacklist.insert_one({'url': img})
        else:
            img = loader.hentai_coll.find_one()[search_parameter]
            loader.hentai_coll.delete_one({'url': img})
            loader.blacklist.insert_one({'url': img})
            caption = ''

        await app.send_photo(chat_id=chat_id, caption=caption, parse_mode=ParseMode.MARKDOWN, photo=img,
                             schedule_date=date)


userbot = Userbot()
