import sqlite3
from sqlite3 import Error 
from random import randint

class dbClass():
    def __init__(self, db_path=r"db.sqlite3", gridHeight=5): 
        self.db_path = db_path
        self.gridHeight = gridHeight 
        self.wordCount = gridHeight * gridHeight
        self.conn = None

        self.create_connection()

    def create_connection(self):
        self.close_connection()
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            print('----- Connection to SQLite Database made -----')
        except Error as e:
            print(e)
        self.conn = conn
        return 

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            print('----- Connection to SQLite Database terminated -----')

    def select_all_words(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM dictionary')

        rows = cur.fetchall();
        print(rows)
        
        for row in rows:
            print(row)

    def insert_word(self, word):
        cur = self.conn.cursor()
        sql = 'INSERT INTO dictionary (word) VALUES ("{}")'.format(word)
        # print(sql)
        cur.execute(sql)
        self.conn.commit()
        return

    def get_room(self, room_code):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM rooms WHERE room_code = {}'.format(room_code))

        row = cur.fetchone()
        description = []
        for name in cur.description:
            description.append(name[0])

        if len(row) > 0:
            room =  {}
            for i in range(len(description)):
               room[description[i]] = row[i]
            return room
        else:
            return

    def create_room(self):
        cur = self.conn.cursor()
        
        randomList = self.generateList()
        redList = randomList[:9]
        blueList = randomList[9:17]
        assassinList = randomList[17:20]
        # print('Reds: ',redList)
        # print('Blues: ',blueList)
        # print('Assassins: ',assassinList)
        redList = ','.join(redList)
        blueList = ','.join(blueList)
        assassinList = ','.join(assassinList)

        sql = "INSERT INTO rooms (red_ids, blue_ids, assassin_ids) VALUES ('{}', '{}', '{}')".format(redList, blueList, assassinList)

        # data = object()
        # data.word_list = word_list
        # cur.execute(sql, data)
        # print(sql)

        cur.execute(sql)
        self.conn.commit()
        newId = cur.lastrowid

        return self.get_room(newId)

    def generateList(self):

        cur = self.conn.cursor()
        cur.execute('SELECT COUNT(*) AS total FROM dictionary')
        total = cur.fetchone();
        total = int(total[0])
        # print('Total: ',total)
        count = 0
        wordIdList = []
        while count < 25:
            id = randint(0, total)
            if(id not in wordIdList):
                wordIdList.append(str(id))
                count+=1
        # print('wordIdList', wordIdList)

        return wordIdList



if __name__ == '__main__':
    newConnection = dbClass()
    room = newConnection.create_room()
    for column in room:
        print(column, room[column])
    newConnection.close_connection()

