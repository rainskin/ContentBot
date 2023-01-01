from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    # Просмотр пикч
    choosing_category = State()
    choosing_amount = State()

    # Загрузка контента
    upload_channel = State()
    collect_pictures = State()

    # Отложка
    schedule = State()
    choosing_days = State()
    choosing_time = State()
    accept = State()
