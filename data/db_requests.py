import sqlite3
import datetime


def time_in_right_form():
    """ Вовращает время в корректном формате

    :return: строка со временем
    """
    date = str(datetime.datetime.today().weekday())
    time = date
    date = str(datetime.datetime.today().hour)
    if len(date) < 2:
        time = time + '0' + date + ':'
    else:
        time = time + date + ':'
    date = str(datetime.datetime.today().minute)
    if len(date) < 2:
        time = time + '0' + date
    else:
        time = time + date
    return time


def choose_users_by_time(db_cursor, time):
    """Возвращает массив с id пользователей, у которых пара начинается в указанное время

    :param db_cursor: курсор базы данных
    :param time: время в корректном формате
    :return: массив с id студентов
    """
    group = cursor.execute('SELECT group_id FROM schedule WHERE ' + time + ' != ""').fetchall()
    students_id = []
    for group_number in range(len(group)):
        one_group_id = db_cursor.execute('SELECT id FROM users WHERE group_number = ' +
                          '"' + group[group_number][0] + '"').fetchall()
        for id_number in range(len(one_group_id)):
            students_id.append(one_group_id[id_number][0])

    return students_id


def add_user_to_table(db_cursor, user_id, group):
    """Добавляет id пользователя в базу данных

    :param db_cursor: курсор базы данных
    :param user_id: id пользователя
    :param group: название группы
    :return: ничего
    """
    note = [user_id, group]
    try:
        db_cursor.execute('INSERT INTO users(id, group_number) VALUES (?, ?)', note)
    except:
        db_cursor.execute('UPDATE users SET group_number =' + '"' + group + '"' +
                          'WHERE id = ' + str(user_id))
        print('note was updated')

