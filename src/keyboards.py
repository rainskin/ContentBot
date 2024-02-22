from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove

from handlers.channels.start_command import show_channels

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


class DelAdmin(InlineKeyboardMarkup):
    button = InlineKeyboardButton('Удалить', callback_data='delete')

    def __init__(self):
        super().__init__()
        self.add(self.button)


def create_channel_buttons(channels):
    buttons = []
    for channel in channels:
        channel = InlineKeyboardButton(text=channel, callback_data=channels[channel]['id'])
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
    channels = show_channels()
    channel_buttons = create_channel_buttons(channels)

    buttons = channel_buttons

    def __init__(self):
        super().__init__()

        row = []
        for button in self.buttons:
            row.append(button)
            if len(row) == 2:
                self.row(*row)
                row = []
        if row:
            self.row(*row)

    def delete_channel(self, channel_id):
        for button in self.buttons:
            if button.callback_data == channel_id:
                self.buttons.remove(button)

    def add_channel(self, title, channel_id):
        channel = InlineKeyboardButton(text=title, callback_data=channel_id)
        self.buttons.append(channel)


class ChannelsWithServiceButtons(Channels, ChannelServiceButtons):
    service_buttons = ChannelServiceButtons.buttons

    def __init__(self):
        super().__init__()

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


class AdPostSettings(InlineKeyboardMarkup):
    sound_on = InlineKeyboardButton('🔔 Со звуком: Да', callback_data='toggle_notification')
    sound_of = InlineKeyboardButton('🔕 Со звуком: Нет', callback_data='toggle_notification')
    enable_author = InlineKeyboardButton('👤 Репост: Да', callback_data='toggle_author')
    disable_author = InlineKeyboardButton('🚷 Репост: Нет', callback_data='toggle_author')

    start_schedule = InlineKeyboardButton('✅ Запланировать', callback_data='start_schedule')
    cancel_btn = InlineKeyboardButton('❌ Отменить', callback_data='cancel')

    def __init__(self, drop_author: bool, notification: bool):
        super().__init__()
        notification_btn = self.sound_on if notification else self.sound_of
        author_btn = self.enable_author if drop_author else self.disable_author
        self.row_width = 2
        self.add(notification_btn, author_btn, self.start_schedule, self.cancel_btn)


class AdDate(InlineKeyboardMarkup):
    today = InlineKeyboardButton('Сегодня', callback_data='today')
    tomorrow = InlineKeyboardButton('Завтра', callback_data='tomorrow')

    def __init__(self):
        super().__init__()
        self.add(self.today, self.tomorrow)


class SaleSettings(InlineKeyboardMarkup):
    schedule_ad_post = InlineKeyboardButton('🕐 Запланировать пост', callback_data='schedule_ad_post')
    schedule_additional_ad_post = InlineKeyboardButton('+ Добавить еще пост', callback_data='schedule_additional_ad_post')

    add_sale_info = InlineKeyboardButton('➕ Добавить инф. о продаже', callback_data='add_sale_info')
    update_sale_info = InlineKeyboardButton('♻️ Обновить инф. о продаже', callback_data='update_sale_info')

    delete_scheduled_posts = InlineKeyboardButton('🗑 Удалить посты', callback_data='delete_scheduled_posts')



    def __init__(self, sale_info=None, ad_is_scheduled=False):
        super().__init__()
        sale_info_btn = self.update_sale_info if sale_info else self.add_sale_info
        schedule_ad_btn = self.schedule_additional_ad_post if ad_is_scheduled else self.schedule_ad_post
        self.row_width = 1

        if ad_is_scheduled:
            self.add(sale_info_btn, schedule_ad_btn, self.delete_scheduled_posts)
        else:
            self.add(sale_info_btn, schedule_ad_btn)
