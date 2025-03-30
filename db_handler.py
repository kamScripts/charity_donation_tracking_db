import sqlite3

class Db_handler:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        
    
    def drop_table(self, table):        
        self.cursor.execute(f'DROP TABLE IF EXISTS {table}')
    def create_table(self, table, values):
        self.drop_table(table)
        query = f'CREATE TABLE {table} ({values});'
        self.cursor.execute(query)
        self.connection.commit()        
        