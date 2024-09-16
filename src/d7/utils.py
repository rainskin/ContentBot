import re
from aiogram import types


def get_msg_html_text(msg: types.Message):
    return re.sub(
        r'<tg-emoji emoji-id="(.*?)">(.*?)</tg-emoji>',
        r"<emoji id=\1>\2</emoji>",
        msg.html_text,
    )
