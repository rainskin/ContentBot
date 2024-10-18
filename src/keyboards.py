from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove

from utils.callback_templates import autodelete_timer_is_template
from utils.time import get_autodelete_time_from_str

delete_btn = InlineKeyboardButton('Удалить', callback_data='delete_photo')
replace_btn = InlineKeyboardButton('Переместить в 🔞', callback_data='replace_photo')
photo_kb = InlineKeyboardMarkup().add(delete_btn, replace_btn)
delete_kb = InlineKeyboardMarkup().add(delete_btn)

test_btn = InlineKeyboardButton('ТЕСТ ЧИ ДА', callback_data='test_btn')
test_kb = InlineKeyboardMarkup().add(test_btn)

category_lite_btn = KeyboardButton('Лайт')
category_18_btn = KeyboardButton('Хентай')

category_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(category_lite_btn, category_18_btn)

remove = ReplyKeyboardRemove()

# Выбор времени для отложки
time_2 = InlineKeyboardButton('0, 15, 19', callback_data='0, 15, 19')
time_3 = InlineKeyboardButton('11, 16, 21 (Alight)', callback_data='11, 16, 21')
time_4 = InlineKeyboardButton('11, 15, 19, 23', callback_data='11, 15, 19, 23')
time_5 = InlineKeyboardButton('10, 13, 16, 19, 22', callback_data='10, 13, 16, 19, 22')
choose_time_kb = InlineKeyboardMarkup(row_width=1).add(time_2, time_3, time_4, time_5)

accept_btn = InlineKeyboardButton('Начать планирование', callback_data='accept')
finish_schedule_kb = InlineKeyboardMarkup().add(accept_btn)

done_btn = KeyboardButton('Готово')
done_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(done_btn)

cancel_btn = InlineKeyboardButton('❌ Отменить', callback_data='cancel')
cancel_current_action = InlineKeyboardButton('❌ Отменить', callback_data='cancel_current_action')


# Yes or No buttons
class YesOrNo(InlineKeyboardMarkup):
    yes_btn = InlineKeyboardButton('Да', callback_data='yes')
    no_btn = InlineKeyboardButton('Нет', callback_data='no')

    def __init__(self):
        super().__init__()
        self.add(self.yes_btn, self.no_btn)


class ConfirmParsing(InlineKeyboardMarkup):
    button = InlineKeyboardButton('Подтвердить', callback_data='ConfirmParsing.button')

    def __init__(self):
        super().__init__()
        self.add(self.button)


class AddOneButton(InlineKeyboardMarkup):

    def __init__(self, button: InlineKeyboardButton):
        super().__init__()
        self.add(button)


class DelAdmin(InlineKeyboardMarkup):
    button = InlineKeyboardButton('Удалить', callback_data='delete')

    def __init__(self):
        super().__init__()
        self.add(self.button)


def create_channel_buttons(channels: list[dict]):
    buttons = []
    for channel_info in channels:
        title = channel_info.get('title')
        _id = channel_info.get('id')

        channel = InlineKeyboardButton(text=title, callback_data=_id)
        buttons.append(channel)

    return buttons


class ChannelServiceButtons(InlineKeyboardMarkup):
    add_channel = InlineKeyboardButton('➕Добавить канал', callback_data='add_channel')
    del_channel = InlineKeyboardButton('🗑Удалить канал', callback_data='del_channel')
    cancel_button = InlineKeyboardButton('❌Отменить', callback_data='cancel')

    buttons = [add_channel, del_channel, cancel_button]

    def __init__(self):
        super().__init__()


class Channels(InlineKeyboardMarkup):

    buttons = None

    def __init__(self, channels: list[dict]):
        super().__init__()

        self.buttons = create_channel_buttons(channels)
        row = []
        for button in self.buttons:
            row.append(button)
            if len(row) == 2:
                self.row(*row)
                row = []
        if row:
            self.row(*row)

    def delete_channel(self, channel_id):
        if not self.buttons:
            return

        for button in self.buttons:
            if button.callback_data == channel_id:
                self.buttons.remove(button)

    def add_channel(self, title, channel_id):
        channel = InlineKeyboardButton(text=title, callback_data=channel_id)
        self.buttons.append(channel)


class ChannelsWithServiceButtons(Channels, ChannelServiceButtons):
    service_buttons = ChannelServiceButtons.buttons

    def __init__(self, channels: list[dict]):
        super().__init__(channels=channels)

        row = []
        for button in self.service_buttons:
            row.append(button)
            if len(row) == 2:
                self.row(*row)
                row = []
        if row:
            self.row(*row)


class NotificationOn(InlineKeyboardMarkup):
    button = InlineKeyboardButton('Со звуком: Да', callback_data='notification_yes')

    def __init__(self):
        super().__init__()
        self.add(self.button)


class NotificationOff(InlineKeyboardMarkup):
    button = InlineKeyboardButton('Со звуком: Нет', callback_data='notification_no')

    def __init__(self):
        super().__init__()
        self.add(self.button)


class InlineKeyboardBuilder(InlineKeyboardMarkup):
    ok_btn = InlineKeyboardButton(text='✅ Готово', callback_data='accept_inline_keyboard')

    def __init__(self, keyboard_data: str, is_preview: bool = False):
        super().__init__()
        rows_data = keyboard_data.strip().split('\n')  # Разделяем по строкам для получения рядов
        for row_data in rows_data:
            buttons = []
            button_datas = [btn.strip() for btn in row_data.strip().split('|')]  # Разделяем ряд по '|'
            for button_data in button_datas:
                if button_data:
                    parts = button_data.strip().split('-', 1)  # Разделяем по первому вхождению '-'
                    if len(parts) == 2:
                        text, link = parts
                        btn = InlineKeyboardButton(text=text.strip(), url=link.strip())
                        buttons.append(btn)
                    else:
                        raise ValueError('Некорректный формат клавитуры')
            self.row(*buttons)
        if is_preview:
            self.add(self.ok_btn)


class AdPostSettings(InlineKeyboardMarkup):
    sound_on = InlineKeyboardButton('🔔 Со звуком: Да', callback_data='toggle_notification')
    sound_of = InlineKeyboardButton('🔕 Со звуком: Нет', callback_data='toggle_notification')
    enable_author = InlineKeyboardButton('👤 Репост: Да', callback_data='toggle_author')
    disable_author = InlineKeyboardButton('🚷 Репост: Нет', callback_data='toggle_author')

    add_inline_keyboard = InlineKeyboardButton('➕ Доб. кнопки', callback_data='add_inline_keyboard')
    remove_inline_keyboard = InlineKeyboardButton('➖ Убрать кнопки', callback_data='remove_inline_keyboard')

    start_schedule = InlineKeyboardButton('✅ Запланировать', callback_data='start_schedule')

    def __init__(self, drop_author: bool, notification: bool, inline_keyboard=False, auto_delete_timer: str = None):
        if auto_delete_timer:
            hour, minutes = get_autodelete_time_from_str(auto_delete_timer)
            autodelete_timer_btn_text = f'Удалить через: {hour}ч {minutes} м'
        else:
            autodelete_timer_btn_text = f'Без удаления'

        set_autodelete_timer = InlineKeyboardButton(autodelete_timer_btn_text, callback_data='set_autodelete_timer')

        super().__init__()
        notification_btn = self.sound_on if notification else self.sound_of
        author_btn = self.enable_author if drop_author else self.disable_author
        inline_keyboard_btn = self.remove_inline_keyboard if inline_keyboard else self.add_inline_keyboard
        self.row(notification_btn, author_btn)
        self.row(inline_keyboard_btn)
        self.row(set_autodelete_timer)
        self.row(self.start_schedule, cancel_btn)


class AutodeleteTimerAmount(InlineKeyboardMarkup):
    callback_template = autodelete_timer_is_template()

    minute_15 = InlineKeyboardButton('15 м', callback_data=f'{callback_template}00:15')
    minute_30 = InlineKeyboardButton('30 м', callback_data=f'{callback_template}00:30')
    hour_1 = InlineKeyboardButton('1 ч', callback_data=f'{callback_template}01:00')
    hour_24 = InlineKeyboardButton('24 ч', callback_data=f'{callback_template}24:00')
    hour_48 = InlineKeyboardButton('48 ч', callback_data=f'{callback_template}48:00')
    hour_72 = InlineKeyboardButton('72 ч', callback_data=f'{callback_template}72:00')
    without_autodelete = InlineKeyboardButton('Без удаления', callback_data=f'without_autodelete')

    def __init__(self):
        super().__init__()
        self.row(self.minute_15, self.minute_30, self.hour_1)
        self.row(self.hour_24, self.hour_48, self.hour_72)
        self.row(self.without_autodelete)


class AdDate(InlineKeyboardMarkup):
    today = InlineKeyboardButton('Сегодня', callback_data='today')
    tomorrow = InlineKeyboardButton('Завтра', callback_data='tomorrow')
    yesterday = InlineKeyboardButton('Вчера', callback_data='yesterday')

    def __init__(self):
        super().__init__()
        self.row_width = 2
        self.add(self.today, self.tomorrow, self.yesterday)


class SaleSettings(InlineKeyboardMarkup):
    schedule_ad_post = InlineKeyboardButton('🕐 Запланировать пост', callback_data='schedule_ad_post')
    schedule_additional_ad_post = InlineKeyboardButton('+ Добавить еще пост',
                                                       callback_data='schedule_additional_ad_post')

    add_sale_info = InlineKeyboardButton('➕ Добавить инф. о продаже', callback_data='add_sale_info')
    update_sale_info = InlineKeyboardButton('♻️ Обновить инф. о продаже', callback_data='update_sale_info')
    delete_sale = InlineKeyboardButton('❌ Удалить продажу', callback_data='delete_sale')

    delete_scheduled_posts = InlineKeyboardButton('🗑 Удалить посты', callback_data='delete_scheduled_posts')

    def __init__(self, sale_info=None, ad_is_scheduled=False):
        super().__init__()
        sale_info_btn = self.update_sale_info if sale_info else self.add_sale_info
        schedule_ad_btn = self.schedule_additional_ad_post if ad_is_scheduled else self.schedule_ad_post
        self.row_width = 1

        if ad_is_scheduled:
            self.add(sale_info_btn, schedule_ad_btn, self.delete_scheduled_posts, self.delete_sale)
        else:
            self.add(sale_info_btn, schedule_ad_btn, self.delete_sale)
