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


bot = telebot.TeleBot('1475926428:AAHcGfNcx0VpOvPkiQt6_1EuRjajyMo86UY')


while True:
    now_time = db_requests.time_in_right_form()
    time_with_delay = db_requests.time_plus_ten_minutes(db_requests.time_in_right_form())
    users = db_requests.choose_users_by_time(time_with_delay)
    if users != []:
        for chat_id in users:
            schedule = db_requests.get_schedule(str(chat_id))
            schedule = schedule[datetime.datetime.today().weekday()]
            lectures = current_lecture(db_requests.time_in_right_form(), schedule).split('\n')
            if db_requests.get_user_subscribe_status(chat_id) == 1:
                for lecture in lectures:
                    kek = lecture[:5]
                    if lecture[:5] == time_with_delay[1:]:
                        bot.send_message(int(chat_id), 'Скоро начнется лекция\n' + lecture)
                        print(lecture)
        time.sleep(60)
    time.sleep(2)