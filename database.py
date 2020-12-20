import sqlite3
from sqlite3 import Error 
from random import randint

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def select_all_words(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM dictionary')

    rows = cur.fetchall();
    print(rows)
    
    for row in rows:
        print(row)

def insert_word(conn, word):
    cur = conn.cursor()
    sql = 'INSERT INTO dictionary (word) VALUES ("{}")'.format(word)
    # print(sql)
    cur.execute(sql)
    conn.commit()
    return

def get_room(conn, room_code):
    cur = conn.cursor()
    cur.execute('SELECT room_code, word_list FROM rooms WHERE room_code = {}').format(room_code)

    rows = cur.fetchall()

    if len(rows) > 0:
        return rows[0]
    else:
        return

def create_room(conn):
    cur = conn.cursor()
    
    randomList = generateList(conn)


    sql = "INSERT INTO rooms (word_list) VALUES ('{}')".format(randomList)

    # data = object()
    # data.word_list = word_list
    
    # cur.execute(sql, data)
    # print(sql)
    cur.execute(sql)
    conn.commit()
    cur.execute('SELECT room_code, word_list FROM rooms ORDER BY room_code DESC LIMIT 1')
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0]
    else:
        return

def generateList(conn):

    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) AS total FROM dictionary')
    total = cur.fetchall();
    total = int(total[0][0])
    # print('Total: ',total)
    count = 0
    wordList = []
    while count < 25:
        id = randint(0, total)
        if(id not in wordList):
            wordList.append(str(id))
            count+=1
    wordList = ",".join(wordList);
    # print('wordList', wordList)
    sql = "SELECT * FROM dictionary WHERE id IN ({})".format(wordList)
    # print(sql)
    cur.execute(sql)

    rows = cur.fetchall();
    # print(rows)
    wordStr = []
    for row in rows:
        wordStr.append(row[1])
    wordStr = ','.join(wordStr)
    # print('wordStr', wordStr)
    return wordStr


def main():
    database = r"db.sqlite3"

    # create a database connection
    conn = create_connection(database)
    with conn:
        return conn


if __name__ == '__main__':
    conn = main()
    # select_all_words(conn)
    print(create_room(conn))

