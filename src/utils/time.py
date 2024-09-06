from calendar import monthrange
from datetime import datetime, timedelta

from aiogram import types

one_day = timedelta(days=1)


def get_current_date():
    return datetime.now().time()


def get_current_datetime():
    c_datetime = datetime.now()

    return {
        'hour': c_datetime.hour,
        'day': c_datetime.day,
        'month': c_datetime.month,
        'year': c_datetime.year,
        'minute': c_datetime.minute,
        'time': str(c_datetime.minute) + ':' + str(c_datetime.second)
    }


def get_number_of_days_in_a_month(current_year: int, current_month: int):
    return monthrange(current_year, current_month)[1]


def create_valid_date(day: int, current_day: int, current_month: int, current_year: int) -> datetime:
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


class RUMonths:
    months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября", "Ноября",
              "Декабря"]

    def date_to_string(self, day: int, month: int):
        date = str(day) + ' ' + self.months[month - 1]

        return date


def is_not_correct_time(hours: int, minutes: int):
    return hours < 0 or hours > 23 or minutes < 0 or minutes > 59


def get_time_from_msg_text(msg: types.Message):
    time = msg.text

    if ':' in time:
        try:
            hour, minutes = time.split(':')

        except ValueError:
            raise ValueError('Используй только цифры')
            # await msg.delete()
            # return

    elif len(time) <= 3:
        try:
            hour = int(time)
            minutes = 0
        except ValueError:
            raise ValueError('Используй только цифры')

    elif 4 <= len(time) <= 5:
        try:
            hour = int(time[:2])
            minutes = int(time[-2:])

        except ValueError:
            raise ValueError('Используй только цифры')
            # await msg.delete()
            # return

    else:
        raise ValueError('Неверный формат времени')
        # await msg.delete()
        # return

    return hour, minutes

def get_autodelete_time_from_str(str_time: str):
    return str_time.split(':')

def str_time_to_seconds(time_str: str) -> int:
    try:
        # Разделяем строку на часы и минуты
        hours, minutes = map(int, time_str.split(':'))
    except ValueError:
        raise ValueError('Неверный формат времени. Используй формат "чч:мм"')
    total_seconds = hours * 3600 + minutes * 60

    return total_seconds

