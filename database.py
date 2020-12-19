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
    
    for row in rows:
        print(row)

def insert_word(conn, word):
    cur = conn.cursor()
    sql = 'INSERT INTO dictionary (word) VALUES ("{}")'.format(word)
    # print(sql)
    cur.execute(sql)
    return

def main():
    database = r"db.sqlite3"

    # create a database connection
    conn = create_connection(database)
    with conn:
        return conn


if __name__ == '__main__':
    main()


