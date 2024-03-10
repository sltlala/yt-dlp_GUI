import sqlite3

presetTableName = "commandPreset"


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def execute(self, query, values):
        self.cursor.execute(query, values)
        self.connection.commit()

    def fetch(self, query, values):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def create_present_table(self):
        self.connection.cursor()
        # cursor = self.connection.cursor()
        # result = cursor.execute('select * from sqlite_master where name = "%s";' % presetTableName)
