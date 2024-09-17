from typing import Awaitable, Callable
from aiogram import Dispatcher, executor
from .userbot import patch_pyrogram

AsyncFunction = Callable[[], Awaitable[None]]


def run_app(dp: Dispatcher, on_startup: AsyncFunction):
    patch_pyrogram()
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=lambda _: on_startup(),
        allowed_updates=[],
    )
