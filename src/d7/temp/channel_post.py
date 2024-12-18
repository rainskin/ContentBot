# TODO: Remove

from aiogram import Dispatcher, types

from d7.database import db
from d7.media_group_collector import collect_media_group


# async def add_keyboard(chat_id: int, msg_id: int, closer_sale_id: ObjectId):
#     keyboard_data = await sales.get_keyboard_data(closer_sale_id)
#     if keyboard_data:
#         kb = InlineKeyboardBuilder(keyboard_data)
#         await bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=kb)


# async def is_same_markers(closer_sale_id: ObjectId, msg_markers: list[str]):
#     closer_sale_msg_markers: list = await sales.get_msg_markers(closer_sale_id)
#     return set(closer_sale_msg_markers) == set(msg_markers)


# async def process_sale(chat_id: int, messages: list[types.Message], sale: dict):
#     channel_ids = sale.get("channel_ids")

#     if chat_id not in channel_ids:
#         return

#     if not messages:
#         return

#     sale_id = sale.get("_id")

#     if not await sales.is_scheduled_post(sale_id):
#         return

#     markers = [get_marker(m) for m in messages]
#     msg_ids = [m.message_id for m in messages]

#     if not await is_same_markers(sale_id, markers):
#         return

#     sale_msg_id, time = await sales.get_sale_msg_id_and_time_by_sale_id(sale_id)
#     autodelete_time = await sales.get_autodelete_time(sale_id)

#     if not autodelete_time:
#         return

#     if not await ad_manager.sale_is_published(sale_msg_id, time):
#         # if await ad_manager.post_is_published(sale_msg_id, time, chat_id, msg_ids):
#         #     return
#         try:
#             await ad_manager.register_published_ad(sale_msg_id, time, autodelete_time)
#         except DuplicateKeyError:
#             return

#     await add_keyboard(chat_id, messages[0].message_id, sale_id)
#     await ad_manager.add_to_published_posts(sale_msg_id, time, chat_id, msg_ids)


async def on_channel_post(msg: types.Message):
    chat_id = msg.chat.id
    if chat_id not in db.channels.get_ids():
        return
    msgs = await collect_media_group(msg)

    # if chat_id not in db.get_ids_of_all_channels():
    #     return


#     messages = await collect_media_group(msg)
#     logging.info(
#         f"Начал обработку в {messages[0].chat.title}, кол-во сообщений {len(messages)}"
#     )
#     date = messages[0].date
#     await ad_manager.save_posts(date, chat_id, messages)

#     closer_sale_id = await sales.get_closer_sale_id(date)

#     if not closer_sale_id:
#         return

#     sale_data = await sales.get_sale_data(closer_sale_id)
#     date = sale_data.get("date")
#     time = sale_data.get("time")

#     sales_for_same_time = await sales.get_all_sales_by_date_and_time(date, time)

#     for sale in sales_for_same_time:
#         await asyncio.create_task(process_sale(chat_id, messages, sale))
#         await asyncio.sleep(3)

#     logging.info(f"Закончил обработку поста в {messages[0].chat.title}")


def register_channel_post_handler(dp: Dispatcher):
    dp.channel_post_handler(content_types=types.ContentType.ANY)(on_channel_post)
