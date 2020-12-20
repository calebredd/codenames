# # Uncomment code below to import csv list of words into sqlite database
# from csv import reader
# import database

# file1 = open('nouns.csv', 'r')
# csvReader = reader(file1)

# conn = database.main()
# for row in csvReader:
#     # print(row)
#     database.insert_word(conn, row[0])
# database.select_all_words(conn)
