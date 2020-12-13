import telebot
import db_requests
import time
import datetime


def current_lecture(time_now, lectures):
    time_now = time_now[1:len(time_now):1]
    time_position_begin = lectures.find(time_now)
    time_position_end = lectures.find('\n')
    if time_position_begin != -1:
        lectures = lectures[time_position_begin:len(lectures):1]
        lectures = lectures[0:time_position_end:1]
    return lectures


bot = telebot.TeleBot('place_token_here')


while True:
    users = db_requests.choose_users_by_time(db_requests.time_in_right_form())
    if users != []:
        for chat_id in users:
            schedule = db_requests.get_schedule(str(chat_id))
            schedule = schedule[datetime.datetime.today().weekday()]
            bot.send_message(int(chat_id), current_lecture(db_requests.time_in_right_form(), schedule))
        time.sleep(60)
    time.sleep(2)