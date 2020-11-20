from pprint import pprint
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


def clear_row(row):
    """Чистит лист от пустых элементов и убирает из ячеек переходы на новую строку

    :param row: входной лист
    :return: отформатированный лист
    """
    # удаление пустых листов
    for counter in range(values['values'].count([])):
        values['values'].remove([])
    # приведение содержмого ячеек в строку без перехода на новую
    for row in values['values']:
        for pos in range(len(row)):
            row[pos] = row[pos].replace('\n', ' ')
    return row


def write_to_file(file_name, list_to_write):
    """Переписывает лист в файл

    :param file_name: название файла
    :param list_to_write: лист, который небходимо переписать
    :return: ничего
    """
    with open('shedule_data.csv', 'w') as table:
        for row in values['values']:
            for pos in range(len(row)):
                if pos != (len(row)):
                    table.write('|')
                table.write(row[pos])
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
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
# переписывание значений таблицы в лист
values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='A1:H61',
    majorDimension='ROWS'
).execute()
exit()