from aiogram import types

from loader import dp
from utils.check_admin_rights import is_superadmin
from utils.db import get_channel_link_by_title, count_content_posts_by_channel


@dp.message_handler(commands='count', state='*')
async def cmd_count(msg: types.Message):
    if not is_superadmin(msg.from_user.id):
        return
    start_message = await msg.answer('Начинаю подсчет...')
    channels_and_amount_posts = await count_content_posts_by_channel()

    channels_and_amount = []
    for i in sorted(channels_and_amount_posts, key=lambda item: item[1], reverse=True):
        title, amount = i[0], i[1]
        marker = get_marker(amount)
        link = await get_channel_link_by_title(title)

        channels_and_amount.append(f'{marker} <b><a href="{link}">{title}</a></b>  — {str(amount)}')

    channels_for_text = "\n".join(channels_and_amount)
    text = f'<b>Текущее количество постов в БД:</b>\n\n{channels_for_text}\n\nНажми /upload, чтобы начать загрузку контента'
    await msg.answer(text, parse_mode='html', disable_web_page_preview=True)
    await start_message.delete()


def get_marker(amount: int) -> str:
    if 0 < amount < 15:
        marker = '🔴'
    elif 15 < amount < 30:
        marker = '🟡'
    elif amount > 30:
        marker = '🟢'
    else:
        marker = '◽️'

    return marker
