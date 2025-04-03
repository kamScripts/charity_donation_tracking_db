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
        
    def get_table_names(self):
        results = self.cursor.execute('SELECT DISTINCT tbl_name FROM sqlite_schema WHERE tbl_name != "sqlite_sequence";')        
        return results.fetchall()
    
    def get_column_names(self, table):        
        table_info = self.cursor.execute(f'PRAGMA table_info({table})')
        #use slicing to remove ID column
        return [column[1] for column in table_info.fetchall()[1:]]
    
    def insert_row(self, table, values):
        placeholders = ', '.join(['?' for _ in enumerate(self.get_column_names(table))])
        query = f'INSERT INTO {table}({", ".join(self.get_column_names(table))}) VALUES({placeholders});'
        print(query)
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print(values, ' inserted')
        except sqlite3.OperationalError as e:
            print(e)
        except sqlite3.IntegrityError as e:
            print(e)
        
    def insert_many(self, table, data):
        placeholders = ','.join(['?' for _ in enumerate(self.get_column_names(table))])
        query = f'INSERT INTO {table}({", ".join(self.get_column_names(table))}) VALUES({placeholders});'
        print(query)
        try:
            self.cursor.executemany(query, data)
            self.connection.commit()
            print('dataset inserted successfully')
        except sqlite3.OperationalError as e:
            print(e)
        except sqlite3.IntegrityError as e:
            print(e)