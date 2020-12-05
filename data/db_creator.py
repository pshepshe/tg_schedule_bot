import sqlite3


connection = sqlite3.connect('users_data.db')

cursor = connection.cursor()
try:
    cursor.execute("CREATE TABLE schedule(group_id text PRIMARY KEY)")
except:
    print('')

try:
    cursor.execute('''CREATE TABLE users(id integer PRIMARY KEY, 
                   group_number text, 
                   FOREIGN KEY(group_number) REFERENCES schedule(group_id))''')
except:
    print('')
with open ('schedule_data.csv','r', encoding='windows-1251') as table:
    row = table.readline()
    row = row.split('|')
    for column in range(2, len(row)):
        cursor.execute('''INSERT INTO schedule(group_id)
        VALUES(?)''', [row[column].replace('\n', '')])
    row[7] = row[7].replace('\n', '')
    stroka = table.readline()
    while stroka != '':
        stroka = stroka.split('|')
        hor_vid = '"' + stroka[0] + stroka[1][0:5:1] + '"'
        cursor.execute('''ALTER TABLE schedule ADD''' + hor_vid)
        for column in range(2, len(row)):
            cursor.execute('''UPDATE schedule SET ''' + hor_vid + '=' + '"' + stroka[column].replace('\n', '') + '"'
                            + ' WHERE group_id = ' + '"' + row[column] + '"')
        stroka = table.readline()

connection.commit()