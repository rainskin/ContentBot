from datetime import datetime as dt
from typing import List

from loader import list_of_channels, sales


def get_ids_of_all_channels():
    return list_of_channels.distinct('id')


def get_channels_title_by_id(ids: List[int]):
    return [list_of_channels.find_one({'id': _id})['title'] for _id in ids]


async def add_sale(
        salesman: str,
        sale_msg_id: int,
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
        'is_main_post': None

    }

    sales.insert_one(sale)


def add_customer_info(sale_msg_id: int, costumer: str, price: int):
    sales.update_one({'sale_msg_id': sale_msg_id}, {"$set": {'costumer': costumer, 'price': price}})


async def add_ad_post_info(sale_msg_id: int, title: str, link: List[str], is_main_post=True):
    link = link[0] if link else None
    sales.update_one({'sale_msg_id': sale_msg_id},
                     {"$set": {'title': title, 'link': link, 'is_main_post': is_main_post}})

# s = {
#     'title': title,
#     'link': link,
#     'is_main_post': is_main_post
# }


