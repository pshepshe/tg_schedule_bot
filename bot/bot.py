import telebot
import datetime

bot = telebot.TeleBot('1475926428:AAHcGfNcx0VpOvPkiQt6_1EuRjajyMo86UY')


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

keyboard_change_course = telebot.types.ReplyKeyboardMarkup()
keyboard_change_course.row('1', '2')
keyboard_change_course.row('3', '4')
keyboard_change_course.row('Назад')


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message)
    bot.send_message(message.chat.id, 'start', reply_markup=keyboard_start)


@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message)
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай')
    elif message.text.lower() == 'стикер':
        bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAO_X7gH9in8dNjxPQxr-yGrckY8tF4AAhkBAAImEKQPn2FCCxlUWG8eBA')
    elif message.text.lower() == 'расписание':
        bot.send_message(message.chat.id, 'Выбери прромежуток времени', reply_markup=keyboard_days)
    elif message.text.lower() in day_of_week:
        day_number = str(day_of_week.index(message.text.lower()))
        bot.send_message(message.chat.id, str(day_number), reply_markup=keyboard_days)
    elif message.text.lower() == 'на сегодня':
        dayweek = datetime.datetime.now().weekday()
        bot.send_message(message.chat.id, str(dayweek), reply_markup=keyboard_days)
    elif message.text.lower() == 'на завтра':
        dayweek = (datetime.datetime.now().weekday() + 1) % 7
        bot.send_message(message.chat.id, str(dayweek), reply_markup=keyboard_days)
    elif message.text.lower() == 'полное расписание':
        bot.send_message(message.chat.id, 'all', reply_markup=keyboard_days)
    elif message.text.lower() == 'выбор группы':
        bot.send_message(message.chat.id, 'Выбери номер курса', reply_markup=keyboard_change_course)
    elif message.text.lower() == 'время':
        bot.send_message(message.chat.id, str(datetime.datetime.now()) + ' ' + str(datetime.datetime.now().weekday()))
    elif message.text.lower() == 'назад':
        bot.send_message(message.chat.id, '-', reply_markup=keyboard_start)
    else:
        bot.send_message(message.chat.id, 'Такая команда не существует')


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)
    print(message.sticker.file_id)
    bot.send_sticker(message.chat.id, message.sticker.file_id)


bot.polling()