import sqlite3


connection = sqlite3.connect('users_data.db')

db_cursor = connection.cursor()
try:
    db_cursor.execute('CREATE TABLE schedule(group_id text PRIMARY KEY)')
except:
    print('')

try:
    db_cursor.execute('''CREATE TABLE users(id integer PRIMARY KEY, 
                   group_number text, subscribe_status bool,
                   FOREIGN KEY(group_number) REFERENCES schedule(group_id))''')
except:
    print('')

with open ('schedule_data2.csv','r', encoding='windows-1251') as table:
    # массив с группами
    groups = table.readline()
    groups = groups.split('|')
    for column in range(2, len(groups)):
        db_cursor.execute('''REPLACE INTO schedule(group_id)
        VALUES(?)''', [groups[column].replace('\n', '')])
    groups[7] = groups[7].replace('\n', '')
    # массив с временем и лекциями в это время
    lectures_current_time = table.readline()
    while lectures_current_time != '':
        lectures_current_time = lectures_current_time.split('|')
        lecture_time = '"' + lectures_current_time[0] + lectures_current_time[1][0:5:1] + '"'
        try:
            db_cursor.execute('ALTER TABLE schedule ADD' + lecture_time)
        except:
            print('')
        for column in range(2, len(groups)):
            db_cursor.execute('UPDATE schedule SET ' + lecture_time + '=' + '"' + lectures_current_time[column].replace('\n', '').replace('"', '') + '"'
                              + ' WHERE group_id = ' + '"' + groups[column] + '"')
        lectures_current_time = table.readline()

connection.commit()
