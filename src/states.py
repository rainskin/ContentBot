from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    choosing_category = State()
    choosing_amount = State()
    schedule = State()
    choosing_days = State()
    choosing_time = State()
