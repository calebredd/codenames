import sqlite3
from sqlite3 import Error 
from random import randint

class dbClass():
    def __init__(self, db_path=r"db.sqlite3", gridHeight=5, assassins=1, reds=9, blues=8): 
        self.db_path = db_path
        self.gridHeight = gridHeight 
        self.wordCount = gridHeight * gridHeight
        self.assassins = assassins
        self.reds = reds
        self.blues = blues
        self.conn = None
        self.cur = None

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
        self.cur = self.conn.cursor()
        return 

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.cur = None
            print('----- Connection to SQLite Database terminated -----')

    def select_all_words(self):
        cur = self.cur
        cur.execute('SELECT * FROM dictionary')

        rows = cur.fetchall();
        print(rows)
        
        for row in rows:
            print(row)

    def insert_word(self, word):
        cur = self.cur
        sql = 'INSERT INTO dictionary (word) VALUES ("{}")'.format(word)
        # print(sql)
        cur.execute(sql)
        self.conn.commit()
        return

    def get_room(self, room_code):
        cur = self.cur
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
        cur = self.cur
        
        randomList = self.generateList()
        base = 0
        redList = randomList[:self.reds]
        base+=self.reds
        blueList = randomList[base:base+self.blues]
        base+=self.blues
        assassinList = randomList[base:base+self.assassins]
        # print('Reds: ',redList)
        # print('Blues: ',blueList)
        # print('Assassins: ',assassinList)
        randomList = ','.join(randomList)
        redList = ','.join(redList)
        blueList = ','.join(blueList)
        assassinList = ','.join(assassinList)

        message = 'New Game'

        sql = "INSERT INTO rooms (guess_count, word_ids, red_ids, blue_ids, assassin_ids, message) VALUES (1, '{}', '{}', '{}', '{}', '{}')".format(randomList, redList, blueList, assassinList, message)

        # data = object()
        # data.word_list = word_list
        # cur.execute(sql, data)
        # print(sql)
        cur.execute(sql)
        self.conn.commit()
        roomId = cur.lastrowid

        return self.get_room(roomId)

    def reveal_word(self, room_code, word):
        cur = self.cur
        room = self.get_room(room_code)
        message = room['message']
        team = room['team_guessing'];
        guesses = room['guess_count'];
        # handle word based on room info
        for wordType in ('assassin_ids', 'red_ids','blue_ids', 'red_guessed', 'blue_guessed', 'neutral_guessed'):
            if room[wordType] is not None:
                room[wordType]=room[wordType].split(',')
            else:
                room[wordType] = []
                # print(room[wordType])
        # print(room)

        # Assassin word, instant death, skull and crossbones
        if word in room['assassin_ids']: 
            if room['team_guessing'] == 'red':
                winner = 'Blue'
                loser = 'Red'
            else:
                winner = 'Red'
                loser = 'Blue'
            message = '{} guessed the Assassin, {} Wins!'.format(loser,winner)
            sql = "UPDATE rooms SET guess_count = 0, assassin_guessed = 1, message='{}' WHERE room_code = {}".format(message, room_code)
            cur.execute(sql)
            self.conn.commit()
            room = self.get_room(room_code)
            return room

        # Red word, point for red, 
        elif word in room['red_ids']:
            if word not in room['red_guessed']: 
                room['red_guessed'].append(word)
                guessed = ','.join(room['red_guessed'])
                if room['team_guessing'] == 'red':
                    if room['guess_count'] is None or room['guess_count']-1 < 1:
                        team = 'blue' #only if guess count is empty
                        guesses = 1
                    else:
                        guesses -= 1
                    message = 'Correct!'
                else:
                    team = 'red'
                    message = "Oops! That was a red tile, your turn is over"
                    guesses = 1
                sql = "UPDATE rooms SET guess_count = '{}', team_guessing = '{}', red_guessed = '{}', message='{}' WHERE room_code = {}".format(guesses, team, guessed, message, room_code)
                # print(sql)
                cur.execute(sql)
                self.conn.commit()
                room = self.get_room(room_code)
            return room
            # if blue guessed, they're turn's over reset guess count
            # elif red guessed, they're turn continues, decrement guess count

        # Blue word, point for blue, 
        elif word in room['blue_ids']: 
            if word not in room['blue_guessed']: 
            # if red guessed, they're turn's over reset guess count
            # elif blue guessed, they're turn continues, decrement guess count
                room['blue_guessed'].append(word)
                guessed = ','.join(room['blue_guessed'])
                if room['team_guessing'] == 'blue':
                    if room['guess_count'] is None or room['guess_count']-1 < 1:
                        team = 'red' #only if guess count is empty
                        guesses = 1
                    else:
                        guesses -= 1
                    message = 'Correct!'
                else:
                    team = 'blue'
                    guesses = 1
                    message = "Oops! That was a blue tile, your turn is over"
                sql = "UPDATE rooms SET guess_count = '{}', team_guessing = '{}', blue_guessed = '{}', message='{}' WHERE room_code = {}".format(guesses, team, guessed, message, room_code)
                # print(sql)
                cur.execute(sql)
                self.conn.commit()
                room = self.get_room(room_code)
            return room

        elif word not in room['neutral_guessed']: # Neutral Id 
            # Update neutral_guessed
            # switch teams and reset guess count
            room['neutral_guessed'].append(word)
            guessed = ','.join(room['neutral_guessed'])
            if room['team_guessing'] == 'blue':
                team = 'red'
            else: team = 'blue'
            message = 'Oops, that is a Neutral tile, your turn is over'
            sql = "UPDATE rooms SET guess_count = 1, team_guessing = '{}', neutral_guessed = '{}', message='{}', guess_count = '{}' WHERE room_code = {}".format(team, guessed, message, room_code, guesses)
            # print(sql)
            cur.execute(sql)
            self.conn.commit()
            room = self.get_room(room_code)
            return room

        else: # Reguess or Bug
            message = 'END of guess iteration reached, undetermined guess response'
            sql = "UPDATE rooms SET message='{}' WHERE room_code = {}".format(message, room_code)
            # print(sql)
            cur.execute(sql)
            self.conn.commit()
            room = self.get_room(room_guess)
            return room

    def generateList(self):

        cur = self.cur
        cur.execute('SELECT COUNT(*) AS total FROM dictionary')
        total = cur.fetchone()
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
        wordIdList = "','".join(wordIdList)
        sql = "SELECT word FROM dictionary WHERE id IN('{}')".format(wordIdList)
        # print(sql)
        cur.execute(sql)
        rows = cur.fetchall()
        wordList = []
        for row in rows:
            wordList.append(row[0])
        return wordList



if __name__ == '__main__':
    newConnection = dbClass()
    room = newConnection.create_room()
    for column in room:
        print(column, room[column])
    words = room['word_ids'].split(',')
    print('words',words)
    redScore=blueScore=count=assassins=0
    redTarget = newConnection.reds
    blueTarget = newConnection.blues
    guesses = []
    while blueScore < blueTarget and redTarget > redScore and room['assassin_guessed'] is None:
        print(room['message'])
        print('Round', count, 'Red:',redScore,'Blue:',blueScore, 'Team:', room['team_guessing'], 'Guesses:', room['guess_count'])
        guess = randint(0,len(words)-1)
        while guess in guesses:
            guess = randint(0,len(words)-1)
        guesses.append(guess)
        word = words[guess]
        print('GUESS #{}'.format(count),'Word:',word)
        room = newConnection.reveal_word(room['room_code'], word)
        if room['red_guessed'] is None:
            room['red_guessed'] = ''
        if room['blue_guessed'] is None:
            room['blue_guessed'] = ''
        redScore = len(room['red_guessed'].split(','))
        blueScore = len(room['blue_guessed'].split(','))
        count+=1
    print(room['message'])
    if blueScore == blueTarget:
        print('Blue WINS!!!')
    if redScore == redTarget:
        print('Red WINS!!!')

    newConnection.close_connection()

