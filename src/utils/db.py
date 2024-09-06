from datetime import datetime as dt, datetime
from typing import List

from loader import list_of_channels, sales, other_channels, ecchi_col, hentai_coll


def get_ids_of_all_channels() -> List[int]:
    return list_of_channels.distinct('id')


def get_channels_title_by_id(ids: List[int]):
    return [list_of_channels.find_one({'id': _id})['title'] for _id in ids]


def get_channel_link_by_title(title: str):
    doc = list_of_channels.find_one({'title': title}, {'link': 1})
    return doc.get('link')


async def add_sale(
        salesman: str,
        sale_msg_id: int,
        sale_msg_text: str,
        date: List[int],
        time: str,
        channel_ids: List[int]
):
    date = '-'.join([str(i) for i in date])
    channels = get_channels_title_by_id(channel_ids)
    sale = {
        'salesman': salesman,
        'costumer': None,
        'price': None,
        'sale_msg_id': sale_msg_id,
        'date': date,
        'time': time,
        'channels': channels,
        'channel_ids': channel_ids,
        'title': None,
        'link': None,
        'scheduled_posts': None,
        'other': {
            'sale_msg_text': sale_msg_text
        }

    }

    sales.insert_one(sale)


async def add_ad_post_info(
        sale_msg_id: int,
        title: str,
        link: List[str],
        keyboard_data: str,
        message_markers: list,
        scheduled_posts: List[tuple],
        autodelete_timer: int,
        is_main_post=True

):
    link = link[0] if link else None
    sales.update_one({'sale_msg_id': sale_msg_id},
                     {"$set":
                         {
                             'title': title,
                             'link': link,
                             'keyboard_data': keyboard_data,
                             'markers': message_markers,
                             'scheduled_posts': scheduled_posts,
                             'is_main_post': is_main_post,
                             'autodelete_timer': autodelete_timer,
                         }}
                     )


async def add_additional_sale(
        sale_msg_id: int,
        date: str,
        time: str,
        title: str,
        keyboard_data: str,
        markers: List[str],
        scheduled_posts: List[tuple],
        autodelete_timer: int
):
    main_sale = sales.find_one({'sale_msg_id': sale_msg_id})
    channel_ids = main_sale['channel_ids']
    channels = get_channels_title_by_id(channel_ids)
    sale = {
        'sale_msg_id': sale_msg_id,
        'date': date,
        'time': time,
        'channels': channels,
        'channel_ids': channel_ids,
        'title': title,
        'keyboard_data': keyboard_data,
        'markers': markers,
        'scheduled_posts': scheduled_posts,
        'autodelete_timer': autodelete_timer,
        'is_main_post': False,
    }

    sales.insert_one(sale)


async def add_ad_additional_posts(
        sale_msg_id: int,
        dt: datetime,
        title: str,
        keyboard_data: str,
        message_markers: list,
        scheduled_posts: List[tuple],
        autodelete_timer):
    day, month, year, hour, minute = dt.day, dt.month, dt.year, dt.hour, dt.minute

    date: str = '{}-{}-{}'.format(str(day), str(month), str(year))
    time: str = '{}:{}'.format(str(hour), str(minute))

    sale = sales.find_one({'sale_msg_id': sale_msg_id})
    exists_post = sale['scheduled_posts']

    grouped_messages = {}

    for chat_id, msg_ids in exists_post:
        if chat_id not in grouped_messages.keys():
            grouped_messages[chat_id] = msg_ids

    for chat_id, msg_ids in scheduled_posts:
        for msg_id in msg_ids:
            grouped_messages[chat_id].append(msg_id)

    result = [(chat_id, msg_ids) for chat_id, msg_ids in grouped_messages.items()]
    sales.update_one({'sale_msg_id': sale_msg_id},
                     {"$set":
                         {
                             'scheduled_posts': result
                         }}
                     )

    await add_additional_sale(sale_msg_id, date, time, title, keyboard_data, message_markers, scheduled_posts,
                              autodelete_timer)


async def add_customer_info(sale_msg_id: int, costumer: str, price: int, title: str):
    sale_msg_text = await get_sale_msg_text(sale_msg_id)
    sales.update_one({'sale_msg_id': sale_msg_id}, {"$set": {'costumer': costumer,
                                                             'price': price,
                                                             'other': {
                                                                 'sale_msg_text': sale_msg_text,
                                                                 'customer_and_price_title': title}
                                                             }
                                                    })


async def get_scheduled_posts(sale_msg_id: int) -> List[tuple]:
    sale = sales.find_one({'sale_msg_id': sale_msg_id})
    return sale['scheduled_posts']


async def delete_scheduled_posts_info(sale_msg_id: int):
    sales.update_one({'sale_msg_id': sale_msg_id},

                     {"$set": {'scheduled_posts': None,
                               'title': None,
                               'link': None,
                               'is_main_post': None,
                               'keyboard_data': None,
                               'markers': None}
                      }
                     )


async def is_sale_info_exist(sale_msg_id: int):
    return bool(sales.find_one({'sale_msg_id': sale_msg_id})['costumer'])


async def is_scheduled_posts_exist(sale_msg_id: int):
    return bool(sales.find_one({'sale_msg_id': sale_msg_id})['scheduled_posts'])


async def get_sale_msg_text(sale_msg_id: int) -> str:
    return sales.find_one({'sale_msg_id': sale_msg_id})['other']['sale_msg_text']


async def get_scheduled_post_datetime(sale_msg_id: int) -> datetime:
    sale = sales.find_one({'sale_msg_id': sale_msg_id})
    date: List[int] = [int(i) for i in sale['date'].split('-')]
    time: List[int] = [int(i) for i in sale['time'].split(':')]
    year, month, day = date[2], date[1], date[0]
    hour, minute = time[0], time[1]
    return datetime(year, month, day, hour, minute)


async def delete_sale(sale_msg_id: int):
    sales.delete_many({'sale_msg_id': sale_msg_id})


async def delete_additional_posts_by_sale_id(sale_msg_id: int):
    sales.delete_many({'sale_msg_id': sale_msg_id, 'is_main_post': False})

async def count_content_posts_by_channel() -> List[tuple]:
    channel_ids = get_ids_of_all_channels()
    channel_title_and_amount = []

    for channel_id in channel_ids:

        channel_title = list_of_channels.find_one({'id': channel_id})['title']

        if 'anime tyans' in channel_title.lower():
            number_of_posts = ecchi_col.count_documents({})

        elif 'vip tyan' in channel_title.lower():
            number_of_posts = hentai_coll.count_documents({})

        else:
            number_of_posts = other_channels.count_documents({'channel_id': channel_id})

        channel_title_and_amount.append((channel_title, number_of_posts))

    return channel_title_and_amount
