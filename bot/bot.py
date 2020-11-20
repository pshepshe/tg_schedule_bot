import telebot

bot = telebot.TeleBot('1475926428:AAHcGfNcx0VpOvPkiQt6_1EuRjajyMo86UY')


keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока', 'Стикер')


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message)
    bot.send_message(message.chat.id, 'start', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message)
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай')
    elif message.text.lower() == 'стикер':
        bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAO_X7gH9in8dNjxPQxr-yGrckY8tF4AAhkBAAImEKQPn2FCCxlUWG8eBA')
    else:
        bot.send_message(message.chat.id, '-')


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)
    print(message.sticker.file_id)
    bot.send_sticker(message.chat.id, message.sticker.file_id)


bot.polling()