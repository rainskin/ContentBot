# TODO: refactor

from asyncio import sleep
from time import time
from aiogram import types, Bot
from d7.database.collections.post_templates import PostButtons, PostTemplateDocument
from d7.database.collections.posts import PostDocument
from d7 import db


async def check_posts_forever(bot: Bot):
    while True:
        try:
            await check_posts(bot)
        except Exception as e:
            print(e)  # TODO: log
        finally:
            await sleep(1)


async def check_posts(bot: Bot):
    posts = await db.posts.get_all()
    for post in posts:
        if not post.published:
            if time() >= post.publish_date:
                await publish_post(bot, post)


async def publish_post(bot: Bot, post: PostDocument):
    template = await db.post_templates.get(post.template_id)
    await send_post(bot, template)
    post.published = True
    await db.posts.save(post)


async def send_post(bot: Bot, template: PostTemplateDocument):
    markup = None
    if template.buttons:
        markup = build_markup(template.buttons)
    if template.type == "text":
        await bot.send_message(template.text, reply_markup=markup)
    raise ValueError("Unsupported post type")


def build_markup(buttons: PostButtons):
    markup = types.InlineKeyboardMarkup()
    for row_buttons in buttons:
        inline_buttons = [
            types.InlineKeyboardButton(i.text, i.url) for i in row_buttons
        ]
        markup.row(*inline_buttons)
    return markup
