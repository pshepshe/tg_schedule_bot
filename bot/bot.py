import telebot
import datetime
import db_requests
import time


bot = telebot.TeleBot('place_token_here')

day_of_week = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']

keyboard_start = telebot.types.ReplyKeyboardMarkup()
keyboard_start.row('/start')
keyboard_start.row('Расписание')
keyboard_start.row('Привет', 'Пока', 'Стикер', 'Время')
keyboard_start.row('Выбор группы')

keyboard_days = telebot.types.ReplyKeyboardMarkup()
keyboard_days.row('Понедельник', 'Вторник', 'Среда')
keyboard_days.row('Четверг', 'Пятница', 'Суббота')
keyboard_days.row('На сегодня', 'На завтра', 'Полное расписание')
keyboard_days.row('Назад')

keyboard_groups = telebot.types.ReplyKeyboardMarkup()
keyboard_groups.row('20.Б01-мкн', '20.Б02-мкн', '20.Б03-мкн')
keyboard_groups.row('20.Б04-мкн', '20.Б05-мкн', '20.Б06-мкн')
keyboard_groups.row('Назад')

keyboard_null = telebot.types.ReplyKeyboardMarkup()
keyboard_null.row('Назад')


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message)
    bot.send_message(message.chat.id, 'start', reply_markup=keyboard_start)


@bot.message_handler(content_types=['text'])
def send_text(message):
    global level_id
    print(message)
    if message.text.lower() == 'назад':
        level_id = '0'
        bot.send_message(message.chat.id, '-', reply_markup=keyboard_start)

    elif level_id == '2_1':
        group = message.text
        db_requests.add_user_to_table(str(message.chat.id), group)

    elif level_id == '0':
        if message.text.lower() == 'привет':
            bot.send_message(message.chat.id, 'Привет')
        elif message.text.lower() == 'пока':
            bot.send_message(message.chat.id, 'Прощай')
        elif message.text.lower() == 'стикер':
            bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAO_X7gH9in8dNjxPQxr-yGrckY8tF4AAhkBAAImEKQPn2FCCxlUWG8eBA')
        elif message.text.lower() == 'время':
            bot.send_message(message.chat.id,
                             str(datetime.datetime.now()) + ' ' + str(datetime.datetime.now().weekday()))
        elif message.text.lower() == 'расписание':
            level_id = '1_1'
            bot.send_message(message.chat.id, 'Выбери прромежуток времени', reply_markup=keyboard_days)
        elif message.text.lower() == 'выбор группы':
            level_id = '2_1'
            bot.send_message(message.chat.id, 'Введите свою группу', reply_markup=keyboard_groups)

    elif level_id == '1_1':
        if message.text.lower() in day_of_week:
            day_number = day_of_week.index(message.text.lower())
            schedule = db_requests.get_schedule(str(message.from_user.id))
            bot.send_message(message.chat.id, schedule[day_number], reply_markup=keyboard_days)
        elif message.text.lower() == 'на сегодня':
            dayweek = datetime.datetime.now().weekday()
            schedule = db_requests.get_schedule(str(message.from_user.id))
            bot.send_message(message.chat.id, schedule[dayweek], reply_markup=keyboard_days)
        elif message.text.lower() == 'на завтра':
            dayweek = (datetime.datetime.now().weekday() + 1) % 7
            schedule = db_requests.get_schedule(str(message.from_user.id))
            bot.send_message(message.chat.id, schedule[dayweek], reply_markup=keyboard_days)
        elif message.text.lower() == 'полное расписание':
            bot.send_message(message.chat.id, 'all', reply_markup=keyboard_days)

    #else:
    #    bot.send_message(message.chat.id, 'Такая команда не существует')


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)
    print(message.sticker.file_id)
    bot.send_sticker(message.chat.id, message.sticker.file_id)


def levelback(id):
    pass


level_id = '0'
bot.polling()