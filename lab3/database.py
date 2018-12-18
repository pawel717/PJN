import mysql.connector
import json

class Database:
    def __init__(self):
        self.db = None
        self.createDbConnection()


    def createDbConnection(self):
        config = json.load(open('config.json'))
        self.db = mysql.connector.connect(
            host=config['mysql']['host'],
            user=config['mysql']['user'],
            passwd=config['mysql']['passwd'],
            database=config['mysql']['database'],
            use_unicode=config['mysql']['use_unicode']
        )

        cursor = self.db.cursor()

        # Enforce UTF-8 for the connection.
        cursor.execute('SET NAMES utf8mb4')
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")

        # Commit data.
        self.db.commit()

        return self.db


    def fetch_data(self, query="SELECT * FROM articles", dictionary=True, buffered=True):
        cursor = self.db.cursor(dictionary=dictionary, buffered=buffered)
        cursor.execute(query)

        print("query '{}' executed\n".format(query))

        return cursor


    def insert_data(self, query, query_args):
        insertCursor = self.db.cursor()
        insertCursor.execute(query, query_args)
        self.db.commit()

        print("query '{}' executed\n".format(query))

        return insertCursor