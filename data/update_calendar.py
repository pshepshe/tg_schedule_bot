import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

groups_calendar = {'20.Б01-мкн': 'dcdq0k481p3ank5cg4nkjauti8@group.calendar.google.com',
                   '20.Б02-мкн': '5mfumtkgj2oucp4i2iaovbhrmo@group.calendar.google.com',
                   '20.Б03-мкн': 'i0sr0lhdmqr7g7tl6hq88cvsgk@group.calendar.google.com',
                   '20.Б04-мкн': '360snk5f76avr6rc59hj8umf7o@group.calendar.google.com',
                   '20.Б05-мкн': '7arbdnu68qijmqp7ah1da1l9so@group.calendar.google.com',
                   '20.Б06-мкн': 'rdbffl2pdj147l6fj615kadlec@group.calendar.google.com'}
# авторизация сервисного аккаунта
CREDENTIALS_FILE = 'creds.json'
calendar_ident = 'dcdq0k481p3ank5cg4nkjauti8@group.calendar.google.com'
spreadsheet_id = '1wk_ekeLOZF0ZFgX25tqLXSnQtFcFcXByXoo9KPX_zUo'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive',
     'https://www.googleapis.com/auth/calendar',
     'https://www.googleapis.com/auth/calendar.events'],
)
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('calendar', 'v3', http=httpAuth)
# шаблон события для записи в календарь
event = {
    "summary": 'test_event',
    "description": 'none',
    'start': {
        'dateTime': '2020-12-20T02:00:00',
        'timeZone': 'Europe/Moscow',
    },
    'end': {
        'dateTime': '2020-12-20T05:00:00',
        'timeZone': 'Europe/Moscow',
    }
}
# удаление прошлых событий из календаря
current_date = datetime.today()
current_day = datetime.today().weekday()

for current_group in groups_calendar:
    page_token = None
    while True:
        events = service.events().list(calendarId=groups_calendar[current_group], pageToken=page_token).execute()
        page_token = events.get('nextPageToken')
        events = events['items']
        for current_event in events:
            event_time = current_event['start']['dateTime'][:10]
            print(event_time)
            event_time = datetime(int(event_time[:4]), int(event_time[5:7]), int(event_time[8:10]))
            if current_date > event_time + timedelta(days=1):
                service.events().delete(calendarId=groups_calendar[current_group], eventId=current_event['id']).execute()
        if not page_token:
            break
# запись расписания в двумерный список
current_date = datetime.today().date()
current_day = datetime.today().weekday()
print(current_date)

with open('schedule_data2.csv', 'r') as schedule:
    groups = schedule.readline().split('|')
    groups[len(groups) - 1] = groups[len(groups) - 1][:len(groups)+2]
    current_line = schedule.readline().split('|')
    schedule_table = []
    while current_line != ['']:
        schedule_table.append(current_line)
        current_line = schedule.readline().split('|')
# цикл для записи в календарь расписания на следующие schedule days
schedule_days = 7
for delta_day in range(schedule_days):
    # номер дня недели, для которого нужно записать расписание
    day = str((int(datetime.today().weekday()) + delta_day) % 7)
    for time_line in schedule_table:
        for group_number in range(len(time_line) - 2):
            page_token = None
            # пробегает по всем выдаваемым странциам событий
            while True:
                current_lecture = time_line[group_number + 2]
                check_event_existence = 0
                # объект datetime для врмени, на которое нужно записать лекцию
                date = current_date + timedelta(days=delta_day)
                current_group = groups[group_number + 2]
                events = service.events().list(calendarId=groups_calendar[current_group], pageToken=page_token).execute()
                # google выдает все события страницами и оставляет nextPageToken для доступа у следующей странице
                page_token = events.get('nextPageToken')
                # проверка на существование одинаковых событий
                for current_event in events['items']:
                    if (current_lecture == current_event['summary']) & (str(date) == current_event['start']['dateTime'][:10]):
                        check_event_existence = 1
                # операция записи собтия в календарь
                if (current_lecture != '') & (current_lecture != '\n') & (check_event_existence == 0) & (time_line[0] == day):
                    event['summary'] = current_lecture
                    event['start']['dateTime'] = str(date) + 'T' + time_line[1][:5] + ':00'
                    event['end']['dateTime'] = str(date) + 'T' + time_line[1][8:] + ':00'
                    current_group = groups[group_number + 2]
                    if groups_calendar[current_group] != '':
                        try:
                            service.events().insert(calendarId=groups_calendar[current_group], body=event).execute()
                        except:
                            print('??')
                if not page_token:
                    break

