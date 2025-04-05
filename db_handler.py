import sqlite3
import pandas

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
        return [column[1] for column in table_info.fetchall()]
    
    def get_by_id(self, table, id):
        query = f'SELECT * FROM {table} WHERE {table}_id = ?;'
        self.cursor.execute(query, (id,))
        data = self.cursor.fetchall()
        try:
            val = pandas.DataFrame(data, columns=self.get_column_names(table)).to_string()
        except ImportError as e:
            print(e)
            val = data
        return val
    
    def get_by_column_value(self, table, column, value, opSign='=', numberOfRows='all'):
        query = f'SELECT * FROM {table} WHERE {column} {opSign} ?;'
        self.cursor.execute(query, (value,))
        data = ''
        try:
            if numberOfRows.lower() == 'all':
                data = self.cursor.fetchall()
        except AttributeError:
            print(f'number of Rows: {numberOfRows}')
        try:
            data =  self.cursor.fetchmany(numberOfRows)
        except TypeError:
            print(f'number of Rows: {numberOfRows}')
        try:
            val = pandas.DataFrame(data, columns=self.get_column_names(table)).to_string()
        except ImportError as e:
            print(e)
            val = data

        return val
    
    def insert_row(self, table, values):
        columns = self.get_column_names(table)[1:]
        placeholders = ', '.join(['?' for _ in enumerate(columns)])
        query = f'INSERT INTO {table}({", ".join(columns)}) VALUES({placeholders});'
        print(query)
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print(f'{values} inserted successfully into {table}')
        except sqlite3.OperationalError as e:
            print(e)
        except sqlite3.IntegrityError as e:
            print(e)
        
    def insert_many(self, table, data):
        columns = self.get_column_names(table)[1:]
        placeholders = ', '.join(['?' for _ in enumerate(columns)])
        query = f'INSERT INTO {table}({", ".join(columns)}) VALUES({placeholders});'
        
        try:
            self.cursor.executemany(query, data)
            self.connection.commit()
            print(f'dataset inserted successfully into {table}')
        except sqlite3.OperationalError as e:
            print(e)
        except sqlite3.IntegrityError as e:
            print(e,f'while inserting into {table}')