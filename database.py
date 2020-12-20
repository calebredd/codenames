import sqlite3
from sqlite3 import Error 

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

def create_room(conn, room_code, word_list):
    cur = conn.cursor()
    sql = 'INSERT INTO rooms (room_code, word_list) VALUES (?,?)'

    data = object()
    data.room_code = room_code
    data.word_list = word_list
    
    cur.execute(sql, data)
    conn.commit()
    
    return get_room(conn, room_code)

def main():
    database = r"db.sqlite3"

    # create a database connection
    conn = create_connection(database)
    with conn:
        return conn


if __name__ == '__main__':
    conn = main()
    select_all_words(conn)
