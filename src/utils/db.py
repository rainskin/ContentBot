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
        'is_main_post': None,
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
        scheduled_posts: List[tuple],
        is_main_post=True,

):
    link = link[0] if link else None
    sales.update_one({'sale_msg_id': sale_msg_id},
                     {"$set":
                         {
                             'title': title,
                             'link': link,
                             'is_main_post': is_main_post,
                             'scheduled_posts': scheduled_posts
                         }}
                     )


async def add_customer_info(sale_msg_id: int, costumer: str, price: int, title: str):
    sale_msg_text = await get_sale_msg_text(sale_msg_id)
    sales.update_one({'sale_msg_id': sale_msg_id}, {"$set": {'costumer': costumer,
                                                             'price': price,
                                                             'other': {
                                                                 'sale_msg_text': sale_msg_text,
                                                                 'customer_and_price_title': title}
                                                             }
                                                    })


async def get_scheduled_posts_info(sale_msg_id: int) -> List[tuple]:
    sale = sales.find_one({'sale_msg_id': sale_msg_id})
    return sale['scheduled_posts']


async def delete_scheduled_posts_info(sale_msg_id: int):
    sales.update_one({'sale_msg_id': sale_msg_id},

                     {"$set": {'scheduled_posts': None,
                               'title': None,
                               'link': None,
                               'is_main_post': None}
                      }
                     )


async def sale_info_is_exist(sale_msg_id: int):
    return bool(sales.find_one({'sale_msg_id': sale_msg_id})['costumer'])


async def scheduled_posts_is_exist(sale_msg_id: int):
    return bool(sales.find_one({'sale_msg_id': sale_msg_id})['scheduled_posts'])


# s = {
#     'title': title,
#     'link': link,
#     'is_main_post': is_main_post
# }

async def get_sale_msg_text(sale_msg_id: int) -> str:
    return sales.find_one({'sale_msg_id': sale_msg_id})['other']['sale_msg_text']
