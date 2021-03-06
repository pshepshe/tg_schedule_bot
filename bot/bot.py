import telebot
import datetime
import db_requests

with open('api_key', 'r') as file_key:
    key = file_key.readline()
    bot = telebot.TeleBot(key)
day_of_week = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']
groups = ['20.Б01-мкн', '20.Б02-мкн', '20.Б03-мкн', '20.Б04-мкн', '20.Б05-мкн', '20.Б06-мкн']
all_groups = []
notifications_status = 'выкл'
notifications = {1: 'вкл', 0: 'выкл'}
zoom = {'101': 'https://us02web.zoom.us/j/384956974?pwd=mkn', '102': 'https://us02web.zoom.us/j/958115833?pwd=mkn',
        '103': 'https://us02web.zoom.us/j/212767337?pwd=mkn', '104': 'https://us02web.zoom.us/j/993690805?pwd=mkn',
        '201': 'https://us02web.zoom.us/j/812916426?pwd=mkn', '202': 'https://us02web.zoom.us/j/933271498?pwd=mkn',
        '203': 'https://us02web.zoom.us/j/811738408?pwd=mkn', '301': 'https://us02web.zoom.us/j/511327649?pwd=mkn',
        '302': 'https://us02web.zoom.us/j/675315555?pwd=mkn', '303': 'https://us02web.zoom.us/j/94638145805?pwd=mkn',
        '304': 'https://us02web.zoom.us/j/91097279226?pwd=mkn'}
groups_calendar = {'20.Б01-мкн': 'https://calendar.google.com/calendar/u/0?cid=ZGNkcTBrNDgxcDNhbms1Y2c0bmtqYXV0aThAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ',
                   '20.Б02-мкн': 'https://calendar.google.com/calendar/u/0?cid=NW1mdW10a2dqMm91Y3A0aTJpYW92YmhybW9AZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ',
                   '20.Б03-мкн': 'https://calendar.google.com/calendar/u/0?cid=aTBzcjBsaGRtcXI3Zzd0bDZocTg4Y3ZzZ2tAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ',
                   '20.Б04-мкн': 'https://calendar.google.com/calendar/u/0?cid=MzYwc25rNWY3NmF2cjZyYzU5aGo4dW1mN29AZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ',
                   '20.Б05-мкн': 'https://calendar.google.com/calendar/u/0?cid=N2FyYmRudTY4cWlqbXFwN2FoMWRhMWw5c29AZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ',
                   '20.Б06-мкн': 'https://calendar.google.com/calendar/u/0?cid=cmRiZmZsMnBkajE0N2w2Zmo2MTVrYWRsZWNAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ'}

keyboard_main = telebot.types.ReplyKeyboardMarkup()
keyboard_main.row('Расписание')
keyboard_main.row('Зум каналы', 'Получить календарь')
keyboard_main.row('Выбор группы', 'Изменить статус уведомлений')

keyboard_start = telebot.types.ReplyKeyboardMarkup()
keyboard_start.row('20.Б01-мкн', '20.Б02-мкн', '20.Б03-мкн')
keyboard_start.row('20.Б04-мкн', '20.Б05-мкн', '20.Б06-мкн')

keyboard_days = telebot.types.ReplyKeyboardMarkup()
keyboard_days.row('Понедельник', 'Вторник', 'Среда')
keyboard_days.row('Четверг', 'Пятница', 'Суббота')
keyboard_days.row('На сегодня', 'На завтра')
keyboard_days.row('Назад')

keyboard_groups = telebot.types.ReplyKeyboardMarkup()
keyboard_groups.row('20.Б01-мкн', '20.Б02-мкн', '20.Б03-мкн')
keyboard_groups.row('20.Б04-мкн', '20.Б05-мкн', '20.Б06-мкн')
keyboard_groups.row('Назад')

keyboard_zoom_channels = telebot.types.ReplyKeyboardMarkup()
keyboard_zoom_channels.row('101', '102', '103', '104')
keyboard_zoom_channels.row('201', '202', '203')
keyboard_zoom_channels.row('301', '302', '303', '304')

keyboard_null = telebot.types.ReplyKeyboardMarkup()
keyboard_null.row('Назад')


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message)
    bot.send_message(message.chat.id, 'Выбери любую группу', reply_markup=keyboard_start)


@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message)
    if message.text.lower() == 'назад':
        bot.send_message(message.chat.id, '-', reply_markup=keyboard_main)

    if message.text in groups:
        group = message.text
        db_requests.add_user_to_table(str(message.chat.id), group)
        bot.send_message(message.chat.id, 'Теперь ваша группа ' + message.text, reply_markup=keyboard_main)

    elif message.text.lower() == 'время':
        bot.send_message(message.chat.id,
                         str(datetime.datetime.now()) + ' ' + str(datetime.datetime.now().weekday()))

    elif message.text.lower() == 'расписание':
        bot.send_message(message.chat.id, 'Выбери прромежуток времени', reply_markup=keyboard_days)

    elif message.text.lower() == 'выбор группы':
        bot.send_message(message.chat.id, 'Введите свою группу', reply_markup=keyboard_groups)

    if message.text.lower() in day_of_week:
        day_number = day_of_week.index(message.text.lower())
        schedule = db_requests.get_schedule(str(message.from_user.id))
        if schedule == 0:
            bot.send_message(message.chat.id, 'Вы не выбрали группу', reply_markup=keyboard_main)
        else:
            bot.send_message(message.chat.id, schedule[day_number], reply_markup=keyboard_main)

    elif message.text.lower() == 'на сегодня':
        dayweek = datetime.datetime.now().weekday()
        if dayweek == 6:
            bot.send_message(message.chat.id, 'это выходной день', reply_markup=keyboard_main)
        else:
            schedule = db_requests.get_schedule(str(message.from_user.id))
            if schedule == 0:
                bot.send_message(message.chat.id, 'Вы не выбрали группу', reply_markup=keyboard_main)
            else:
                bot.send_message(message.chat.id, schedule[dayweek], reply_markup=keyboard_main)

    elif message.text.lower() == 'на завтра':
        dayweek = (datetime.datetime.now().weekday() + 1) % 7
        if dayweek == 6:
            bot.send_message(message.chat.id, 'это выходной день', reply_markup=keyboard_days)
        else:
            schedule = db_requests.get_schedule(str(message.from_user.id))
            if schedule == 0:
                bot.send_message(message.chat.id, 'Вы не выбрали группу', reply_markup=keyboard_main)
            else:
                bot.send_message(message.chat.id, schedule[dayweek], reply_markup=keyboard_main)

    elif message.text.lower() == 'зум каналы':
        bot.send_message(message.chat.id, 'Выберите зум канал', reply_markup=keyboard_zoom_channels)

    elif message.text.lower() in zoom:
        bot.send_message(message.chat.id, zoom[message.text], reply_markup=keyboard_main)

    elif message.text.lower() == 'получить календарь':
        user_group = db_requests.get_users_group(str(message.from_user.id))[0]
        if user_group == 0:
            bot.send_message(message.chat.id, 'Вы не выбрали группу', reply_markup=keyboard_main)
        else:
            bot.send_message(message.chat.id, groups_calendar[user_group], reply_markup=keyboard_main)

    elif message.text.lower() == 'изменить статус уведомлений':
        status = db_requests.get_user_subscribe_status(str(message.from_user.id))
        if status == 'no':
            bot.send_message(message.chat.id, 'Необходимо сначала выбрать группу')
        else:
            if status == 1:
                bot.send_message(message.chat.id, 'Уведомления: отключены')
                db_requests.unsubscribe(str(message.from_user.id))
            else:
                bot.send_message(message.chat.id, 'Уведомления: включены')
                db_requests.subscribe(str(message.from_user.id))


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)
    print(message.sticker.file_id)
    bot.send_sticker(message.chat.id, message.sticker.file_id)


bot.polling()