import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


week = {"ПОНЕДЕЛЬНИК": 0, "ВТОРНИК": 1, "СРЕДА": 2, "ЧЕТВЕРГ": 3, "ПЯТНИЦА": 4, "СУББОТА": 5, "День": 'День'}


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


# авторизация сервисного аккаунта
CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1wk_ekeLOZF0ZFgX25tqLXSnQtFcFcXByXoo9KPX_zUo'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
# переписывание значений таблицы в лист
values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='A1:H61',
    majorDimension='ROWS'
).execute()

values = clear_row(values)

values['values'].pop(16)

write_to_file('schedule_data.csv', values)
exit()



