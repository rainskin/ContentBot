import calendar
from datetime import datetime, timedelta
from calendar import monthrange

from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, bot
from states import States

one_day = timedelta(days=1)

current_hour = datetime.now().hour

current_day = datetime.now().day
current_year = datetime.now().year
current_month = datetime.now().month

number_of_days_in_a_month = monthrange(current_year, current_month)[1]

test_date_1 = datetime(year=2024, month=current_month, day=current_day, hour=14)
test_date_2 = datetime(year=2024, month=current_month, day=current_day, hour=15)


def create_valid_date(day: int) -> datetime:
    """This function takes an integer representing a day and returns a valid date. If the provided day is greater
    than or equal to the current day, the function returns a date within the current month. If the day is less than
    the current day, it returns a date in the next month or the next year if the current month is December."""

    if day > current_day:
        return datetime(year=current_year, month=current_month, day=day)

    if day == current_day:
        return datetime(year=current_year, month=current_month, day=current_day)

    if current_month == 12:
        month = 1
        year = current_year + 1
        return datetime(year=year, month=month, day=day)

    month = current_month + 1

    next_date = datetime(year=current_year, month=month, day=1)
    number_of_days_in_a_next_month = monthrange(next_date.year, next_date.month)[1]

    if day <= number_of_days_in_a_next_month:
        date = datetime(year=current_year, month=month, day=day)

    else:
        date = datetime(year=current_year, month=month, day=number_of_days_in_a_next_month)

    return date


RU_MONTHS_GEN = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября",
                 "Ноября", "Декабря"]


class RUMonths():
    months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября", "Ноября",
              "Декабря"]

    def date_to_string(self, day: int, month: int):
        date = str(day) + ' ' + self.months[month - 1]

        return date


def is_not_correct_time(hours: int, minutes: int):
    return hours < 0 or hours > 23 or minutes < 0 or minutes > 59
