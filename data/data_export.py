from pprint import pprint
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


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


def write_to_file(file_name, list_to_write):
    """Переписывает лист в файл с разделителем '|'

    :param file_name: название файла
    :param list_to_write: лист, который небходимо переписать
    :return: ничего
    """
    with open(file_name, 'w') as table:
        for row in list_to_write['values']:
            for pos in range(len(list_to_write['values'][0])):
                if pos < (len(row)):
                    table.write('|')
                if pos < len(row):
                    table.write(row[pos])
                if (pos >= len(row)) and (len(row)) == 3:
                    table.write('|')
                    table.write(row[2])
                if (pos >= len(row)) and (len(row)) == 2:
                    table.write('|')
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
write_to_file('shedule_data.csv', values)
exit()