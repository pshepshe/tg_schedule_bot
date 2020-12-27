import re
from googleapiclient.discovery import build
from oauth2client import file as oauth_file, client, tools


week = {"ПОНЕДЕЛЬНИК": 0, "ВТОРНИК": 1, "СРЕДА": 2, "ЧЕТВЕРГ": 3, "ПЯТНИЦА": 4, "СУББОТА": 5, "День": 'День'}


def row_only_with_time(columns):
    """Создает пустой список длины columns

    :param columns: длина списка
    :return: список с пустыми строками
    """
    row = []
    for elements in range(columns):
        row.append('')
    return row


def add_row_without_duplicate(schedule_table, row, column_n, row_n):
    """ Вставляет в список с расписанием лекцию, исходя из игформации о ее времени начала

    :param schedule_table: список с расписанием
    :param row: ряд, в котором содержится информация о расписании и самой лекции
    :param column_n: номер колонки с лекцией
    :param row_n: номер ряда, на котором находится функция записи расписания в файл
    :return: два значения, где первое говорит произошла ли операция добавления, а вотрое - это имененный список с
    расписанием
    """
    for row_number in range(len(schedule_table)):
        if (row[1] in schedule_table[row_number]) & (row_number >= row_n - 1):
            schedule_table[row_number][column_n] = row[column_n]
            return 1, schedule_table
    return 0, schedule_table


def time_of_lecture_end(time):
    """Прибовляет к времени время одной пары и возвращает значение времени в формате string

    :param time: время формата hh:mm
    :return: время формата hh:mm
    """
    minute = int(time[4]) + 5
    if minute >= 10:
        time = time[:3] + str(int(time[3]) + 1) + '0'
    else:
        time = time[:4] + str(int(time[4]) + 5)
    minute = int(time[3]) + 3
    if minute >= 6:
        time = time[:1] + str(int(time[1]) + 1) + ':' + str(int(time[3]) + 3 - 6) + time[4]
    else:
        time = time[:3] + str(minute) + time[4]
    hour = int(time[1]) + 1
    if hour >= 10:
        time = str(int(time[0]) + 1) + '0' + time[2:]
    else:
        time = time[0] + str(int(time[1]) + 1) + time[2:]
    return time


def lectures_right_time(schedule_table):
    """Проверяет таблицу с расписанием на наличие дополнительной информации о начале лекции и редактирует спсиок с
    с расписанием на основе этой информации

    :param schedule_table: двумерный список с расписанием
    :return: двумерный список с учетом дополнительной информации о начале лекций
    """
    added_rows = 0
    for row_number in range(len(schedule_table)):
        row_number += added_rows
        for column_number in range(len(schedule_table[row_number])):
            cell = schedule_table[row_number][column_number]
            time_position = re.search(r'[св] \w\w[-:]\w\w', cell)
            if time_position != None:
                time_position_start = time_position.span()[0]
                time_position_end = time_position.span()[1]
                time = cell[time_position_start+2:time_position_end:1]
                new_row = row_only_with_time(21)
                new_row[1] = time.replace('-', ':') + ' - ' + time_of_lecture_end(time).replace('-', ':')
                #new_row[1] = new_row[1]
                new_row[column_number] = cell
                complete_check, schedule_table = add_row_without_duplicate(schedule_table, new_row, column_number, row_number)
                schedule_table[row_number][column_number] = ''
                if complete_check != 1:
                    #new_row[1] = new_row[1] + ' - ' + time_of_lecture_end(time).replace('-', ':')
                    schedule_table.insert(row_number + 1, new_row)
                    added_rows += 1
    return schedule_table


def clear_schedule(table):
    """Чистит список с расписанием от пустых элементов и убирает из ячеек переходы на новую строку

    :param table: входной лист
    :return: отформатированный лист
    """
    # удаление пустых листов
    for counter in range(table.count([])):
        table.remove([])
    # приведение содержмого ячеек в строку без перехода на новую
    for row in table:
        for pos in range(len(row)):
            row[pos] = row[pos].replace('\n', ' ').replace('\r', ' ')
    for row in table:
        if row[1] == '':
            table.remove(row)
    return table


def get_false_positions(table):
    """ Возвращает массив с номерами колонок, которые не нужно записывать

    :param table: список с расписанием
    :return: массив номеров колонок, которые не нкжно записывать
    """
    false_positions = []
    for current_position in range(len(table[0])):
        if ((table[0][current_position] == 'День') or (table[0][current_position] == 'Время')) and (current_position > 1):
            false_positions.append(current_position)
    return false_positions


def write_row(row, file, false_columns):
    """Записывает строку таблицы в файл на основании количества объединенных ячеек, стоящих подряд

    :param file: дескриптор файла, в который производится запись
    :param row: строка таблицы
    :return: ничего
    """
    for lecture_number in range(len(row) - 1):
        if (lecture_number + 1) in false_columns:
            print('bb')
        else:
            file.write('|')
            file.write(row[lecture_number + 1])


def write_to_file(file_name, list_to_write):
    """Переписывает лист в файл с разделителем '|'

    :param file_name: название файла
    :param list_to_write: лист, который небходимо переписать
    :return: ничего
    """
    false_columns = get_false_positions(list_to_write)
    with open(file_name, 'w') as table:
        day = list_to_write[0][0]
        for row in list_to_write:
            if row[0] == '':
                table.write(str(week[day]))
            else:
                day = row[0]
                table.write(str(week[day]))
            write_row(row, table, false_columns)
            table.write('\n')
    return 0


# авторизация
SCOPES = ['https://www.googleapis.com/auth/script.projects',
          'https://www.googleapis.com/auth/spreadsheets.currentonly',
          'https://www.googleapis.com/auth/spreadsheets']
store = oauth_file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credenti.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('script', 'v1', credentials=creds)

script_id = '12PnuBrX1CIKwIjJyyoe-UWh0Fyo7roJW-or0jQEx0NeCJaIvbaeGUgcA'

request = {"function": "create_table"}

response = service.scripts().run(body=request, scriptId=script_id).execute()
schedule = response['response']['result']
print(schedule)
print(clear_schedule(schedule))
print(lectures_right_time(schedule))
write_to_file('schedule_data2.csv', schedule)


