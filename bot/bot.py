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
        group = message.text.lower()
        if chek_group(group):    # проверка группы
            level_id = '0'
            bot.send_message(message.chat.id, 'correct', reply_markup=keyboard_start)
            full_group = group.upper() + '-мкн'
            print(message.from_user.id, group, full_group)
        else:
            bot.send_message(message.chat.id, 'Такой группы не существует')
            bot.send_message(message.chat.id, 'Попробуйте ещё раз')

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
            bot.send_message(message.chat.id, 'Введите свою группу', reply_markup=keyboard_null)

    elif level_id == '1_1':
        if message.text.lower() in day_of_week:
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

    #else:
    #    bot.send_message(message.chat.id, 'Такая команда не существует')


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)
    print(message.sticker.file_id)
    bot.send_sticker(message.chat.id, message.sticker.file_id)


def levelback(id):
    pass


def chek_group(group):   # после слиянии кода бота с бд функция будет другой
    actual_groups = {'20': ['01', '02', '03', '04', '05', '06', '09', '10'], '19': ['01', '02', '03', '05', '09', '10'],
                     '18': ['01', '02', '03', '09', '10'], '17': ['01', '02']}
    if group.count('.б') != 1:
        return False
    year, number = group.split('.б')
    if year in actual_groups.keys() and number in actual_groups[year]:
        return True
    return False

level_id = '0'
bot.polling()