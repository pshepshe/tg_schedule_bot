import sqlite3
import datetime
import sqlalchemy
from os import path


working_directory = path.abspath('bot.py').replace('bot\\bot.py', 'data\\users_data.db')
print(working_directory)


def time_in_right_form():
    """ Вовращает текущее время в корректном формате
    :return: строка со временем
    """
    day = str(datetime.datetime.today().weekday())
    time = day + str(datetime.datetime.today())[11:16]
    return time


def sub_create():
    '''Устанавливает статус подписки 0 для пользователя; здесь и далее:
    1 -- пользователь подписан на рассылку
    0 -- пользователь не подписан на рассылку'''

    connection = sqlite3.connect(working_directory)
    db_cursor = connection.cursor()
    db_cursor.execute('''UPDATE users SET subscribe_status = 0 WHERE subscribe_status != 0''')
    connection.commit()
    connection.close()


def subscribe(user_id):
    '''Подписывает пользователя на рассылку'''
    connection = sqlite3.connect(working_directory)
    db_cursor = connection.cursor()
    db_cursor.execute('''UPDATE users SET subscribe_status = 1 WHERE id = ''' + '"' + user_id + '"')
    connection.commit()
    connection.close()


def unsubscribe(user_id):
    """Отписывает пользователя от рассылки"""
    connection = sqlite3.connect(working_directory)
    db_cursor = connection.cursor()
    db_cursor.execute('''UPDATE users SET subscribe_status = 0 WHERE id = ''' + '"' + user_id + '"')
    connection.commit()
    connection.close()


def all_subscribed_users(user_id):
    '''Казалось бы, достает всех подписанных пользователей, но на деле -- делает, что хочет'''
    connection = sqlite3.connect('working_directory')
    db_cursor = connection.cursor()
    db_cursor.execute('''SELECT subscribe_status FROM users WERE subscribe_status = 1''')
    subscribed_users = db_cursor.fetchall()


def get_user_subscribe_status(user_id):
    connection = sqlite3.connect(working_directory)
    db_cursor = connection.cursor()
    subscribe_status = db_cursor.execute('SELECT subscribe_status FROM users WHERE id = ' + user_id).fetchone()
    return subscribe_status[0]

def time_plus_ten_minutes(time):
    minute = int(time[4]) + 1
    if minute >= 6:
        time = time[:4] + '0' + time[5]
        hour = int(time[2]) + 1
    else:
        time = time[:4] + str(minute) + time[5]
        hour = int(time[2])
    if hour >= 10:
        time = time[0] + str(int(time[1]) + 1) + '0' + time[3:]
    else:
        time = time[:2] + str(hour) + time[3:]
    return time


def choose_users_by_time(time):
    """Возвращает массив с id пользователей, у которых пара начинается в указанное время
    :param time: время в корректном формате(строка вида номер дня недели + время). Пример: '009:30' - будет означать
    09:30 понедельника.
    :return: массив с id студентов
    """
    connection = sqlite3.connect(working_directory)
    db_cursor = connection.cursor()
    list_of_times = db_cursor.execute('PRAGMA table_info(schedule)').fetchall()
    check = 0
    for columns in list_of_times:
        if time in columns:
            check = 1
    if check != 0:
        group = db_cursor.execute('SELECT group_id FROM schedule WHERE ' + '"' + time + '"' + ' != ""').fetchall()
    else:
        group = []
    students_id = []
    for group_number in range(len(group)):
        one_group_id = db_cursor.execute('SELECT id FROM users WHERE group_number = ' +
                                         '"' + group[group_number][0] + '"').fetchall()
        for id_number in range(len(one_group_id)):
            students_id.append(one_group_id[id_number][0])
    connection.close()
    return students_id


def add_user_to_table(user_id, group):
    """Добавляет id пользователя и его группу в базу данных
    :param user_id: id пользователя
    :param group: название группы
    :return: ничего
    """
    connection = sqlite3.connect(working_directory)
    db_cursor = connection.cursor()
    note = [user_id, group]
    try:
        db_cursor.execute('INSERT INTO users(id, group_number) VALUES (?, ?)', note)
        subscribe(user_id)
    except:
        db_cursor.execute('UPDATE users SET group_number =' + '"' + group + '"' +
                          'WHERE id = ' + str(user_id))
        print('note was updated')
    connection.commit()
    connection.close()


def get_schedule(user_id):
    """ Выводит расписание в виде двумерного массива вида schedule[a], где a - принимает значения от 0 до 6 и каждая
    цифра, начиная с 0 означает день недели.
    :param user_id: id пользователя, который принимается в виде строки
    :return: список с расписанием или 0, если у пользователя не выбрана группа
    """
    # массив с информацией о стобцах
    connection = sqlite3.connect(working_directory)
    db_cursor = connection.cursor()
    group = db_cursor.execute('SELECT group_number FROM users WHERE id =' + user_id).fetchall()
    if group == []:
        return 0
    group = '"' + group[0][0] + '"'
    list_of_time = db_cursor.execute('PRAGMA table_info(schedule)').fetchall()
    counter_of_lectures = 1
    schedule = []
    for day_of_week in range(6):
        schedule.append('')
        while list_of_time[counter_of_lectures][1][0] == str(day_of_week):
            current_time = list_of_time[counter_of_lectures][1]
            current_lecture = db_cursor.execute('SELECT ' + '"' + current_time + '"' +
                                                ' FROM schedule WHERE group_id = ' + group).fetchall()[0][0]
            # для исключения из листа промежутков отсутствия лекций
            if current_lecture != '':
                schedule[day_of_week] = schedule[day_of_week] + current_time[1:6:1] + ' ' + current_lecture + '\n'
            counter_of_lectures += 1
            if counter_of_lectures >= len(list_of_time):
                break
    connection.close()
    return schedule


def get_users_group(user_id):
    """ Возвращает группу пользователя или 0, если она не выбрана

    :param user_id: id пользователя
    :return: группу пользователя или 0, если она не выбрана
    """
    connection = sqlite3.connect(working_directory)
    db_cursor = connection.cursor()
    group = db_cursor.execute('SELECT group_number FROM users WHERE id =' + user_id).fetchone()
    connection.close()
    if group == []:
        return 0
    return group