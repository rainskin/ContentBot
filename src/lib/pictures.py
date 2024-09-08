# import models
import image
import loader
from . import scraper


def save(pictures: list[str]):
    for picture in pictures:
        item = {'url': picture}
        loader.ecchi_col.insert_one(item)


async def get_new() -> list[str]:
    print('пробую набрать пикчи')
    scraped_pictures = await scraper.get_pictures()
    print(f'собранные пикчи  = {scraped_pictures}')
    new_pictures = []
    for i in scraped_pictures:
        if image.is_new(i):
            new_pictures.append(i)

    return new_pictures
