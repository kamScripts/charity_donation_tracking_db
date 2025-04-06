import sqlite3
import pandas
from db_basic import Db_basic

class Db_handler(Db_basic):
    def __init__(self, db_path):
        super().__init__(db_path)


    def get_by_column_value(self, table, column, value, opSign='=', numberOfRows='all'):
        """view records based on one condition."""
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
    
    def get_total_donations_by_id(self):
        """get donations data"""
        query = """
        SELECT donation.donor_id, first_name, last_name, SUM(amount) AS total_donations
        FROM donation 
        LEFT JOIN donor ON donation.donor_id=donor.donor_id 
        GROUP BY donation.donor_id 
        ;"""
        self.cursor.execute(query)
        tb = pandas.read_sql_query(query, self.connection)
        
        return tb.to_string()


    def get_all(self,table):
        return self.get_all_related_data(table).to_string()
    def get_donor_info(self):
        donor_info = self.get_all_related_data('donor')
        name_city =donor_info[['first_name', 'city_name']]
        return name_city.head()
    def insert_row_all_columns(self, table, values: tuple):
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