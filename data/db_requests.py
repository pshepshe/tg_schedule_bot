import sqlite3
import datetime


def time_in_right_form():
    """ Вовращает текущее время в корректном формате

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
    group = db_cursor.execute('SELECT group_id FROM schedule WHERE ' + time + ' != ""').fetchall()
    students_id = []
    for group_number in range(len(group)):
        one_group_id = db_cursor.execute('SELECT id FROM users WHERE group_number = ' +
                          '"' + group[group_number][0] + '"').fetchall()
        for id_number in range(len(one_group_id)):
            students_id.append(one_group_id[id_number][0])
    return students_id


def add_user_to_table(db_cursor, user_id, group):
    """Добавляет id пользователя и его группу в базу данных

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


def get_schedule(db_cursor, user_id):
    """ Выводит расписание в виде двумерного массива вида schedule[a], где a - принимает значения от 0 до 6 и каждая
    цифра, начиная с 0 означает день недели.

    :param db_cursor: курсор базы данных
    :param user_id: id пользователя, который принимается в виде строки
    :return: лист с расписанием
    """
    # массив с информацией о стобцах
    group = db_cursor.execute('SELECT group_number FROM users WHERE id =' + user_id).fetchall()
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
    return schedule


connection = sqlite3.connect('users_data.db')
cursor = connection.cursor()

add_user_to_table(cursor, 123, '20.Б01-мкн')
connection.commit()
# пример работы
b = get_schedule(cursor, str(123))
print(b[0])
