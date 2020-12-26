import httplib2
import apiclient
import re
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import errors
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools


week = {"ПОНЕДЕЛЬНИК": 0, "ВТОРНИК": 1, "СРЕДА": 2, "ЧЕТВЕРГ": 3, "ПЯТНИЦА": 4, "СУББОТА": 5, "День": 'День'}


def row_only_with_time(columns):
    """Создает пустой лист длины columns

    :param columns: длина листа
    :return: лист с пустыми строками
    """
    row = []
    for elements in range(columns):
        row.append('')
    return row


def add_row_without_duplicate(schedule_table, row, column_n, row_n):
    """

    :param schedule_table:
    :param row:
    :return:
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




def find_changes(schedule_table):
    """Проверяет таблицу с расписанием на наличие дополнительной информации о начале лекции

    :param schedule_table: двумерный список с расписанием
    :return: двумерный список с учетом дополнительной информации
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
                new_row = row_only_with_time(8)
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


def clear_row(table):
    """Чистит лист от пустых элементов и убирает из ячеек переходы на новую строку

    :param table: входной лист
    :return: отформатированный лист
    """
    # удаление пустых листов
    for counter in range(table['values'].count([])):
        table['values'].remove([])
    # приведение содержмого ячеек в строку без перехода на новую
    for row in table['values']:
        for pos in range(len(row)):
            row[pos] = row[pos].replace('\n', ' ')
    return table


def write_row(row, settings, file):
    """Записывает строку таблицы в файл на основании количества объединенных ячеек, стоящих подряд

    :param file: дескриптор файла, в который производится запись
    :param row: строка таблицы
    :param settings: параметры записи в виде листа, который содержит количество объединенных ячеек
    :return: ничего
    """
    position = 0
    for number_of_merged_cells in settings:
        position += 1
        for counter in range(number_of_merged_cells):
            file.write('|')
            if position < len(row):
                file.write(row[position])


def row_type(row, number_of_groups):
    """ Принимает строку таблицы и возвращает лист, в котором последовательно содержится количество объединенных ячеек

    :param number_of_groups: количество групп, для которых имеется предмет в row
    :param row: строка таблицы, в виде лист
    :return: лист с настройками для записи
    """
    setting_list = []
    for counter in range(number_of_groups + 1):                 # дефолтная строка на основании длины строки
        setting_list.append(1)
    if len(row) == 3:
        setting_list = [1, number_of_groups]
        return setting_list
    if len(row) > 3:
        if row[2].find('Иcтория') != -1:                        # обнаружение истории пераого курса
            setting_list = [1, 4, 2]
            return setting_list
        if row[len(row)-1].find('объектно') != -1:              # обнаружение лекций ООП первого курса
            setting_list = [1, 1, 1, 1, 1, 2]
            return setting_list
        else:
            return setting_list

    else:
        return setting_list


def write_to_file(file_name, list_to_write):
    """Переписывает лист в файл с разделителем '|'

    :param file_name: название файла
    :param list_to_write: лист, который небходимо переписать
    :return: ничего
    """
    with open(file_name, 'w') as table:
        day = list_to_write['values'][0][0]
        for row in list_to_write['values']:
            if row[0] == '':
                table.write(str(week[day]))
            else:
                day = row[0]
                table.write(str(week[day]))
            write_row(row, row_type(row, 6), table)
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
print(response)


