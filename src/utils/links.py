from typing import List

from aiogram import types


async def get_links_from_msg(msg: types.Message):
    """
    Returns unique links from a given message

    :param msg:
    :return:
    """
    text = msg.text or msg.caption
    entities = msg.entities or msg.caption_entities
    links = []

    for entity in entities:
        if entity.type == 'url':
            link = text[entity.offset:entity.offset + entity.length]
        elif entity.type == 'text_link':
            link = entity['url']
        else:
            continue

        if link in links:
            continue
        links.append(link)

    return links


def add_links_to_titles(titles: List[str], links: List[str]) -> List[str]:
    channels_with_links = []
    for i in range(len(titles)):
        channels_with_links.append(f'{i + 1}. <b><a href="{links[i]}">{titles[i]}</a></b>')
    return channels_with_links



