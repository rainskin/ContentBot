from aiogram import types
from aiogram.dispatcher import FSMContext
from d7.database.collections.post_templates import (
    PostButton,
    PostButtons,
)
from d7.media_group_collector import collect_media_group
from d7.database import db
from d7.utils import get_msg_html_text


async def on_post_message(msg: types.Message, state: FSMContext):
    msgs = await collect_media_group(msg)
    if not msgs:
        return
    html_text = get_msg_html_text(msg)
    buttons: PostButtons = [[PostButton("test", "https://t.me/test")]]
    files = []
    doc = await db.post_templates.create(
        html_text,
        "text",
        files,
        buttons,
    )
    await state.update_data(post_template_id=doc.id)
    await msg.answer("Готово")


async def on_finish(msg: types.Message, state: FSMContext):
    state_data = await state.get_data()
    post_template_id = state_data["post_template_id"]
    await db.posts.create(post_template_id, 0, 1)
    await msg.answer("Готово")
