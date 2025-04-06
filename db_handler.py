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
    def get_donations_by_id(self, donor, args=None):
        """get donations data"""
        query = f"""
        SELECT DISTINCT donation.donor_id, first_name, last_name, SUM(amount)
        FROM donation 
        LEFT JOIN donor ON donation.donor_id=donor.donor_id 
        GROUP BY donation.donor_id HAVING donation.donor_id={donor}
        ;"""
        self.cursor.execute(query)
        val = self.cursor.fetchall()
        return pandas.DataFrame(val).to_string()
    
    def add_join_string(self, table, current_alias=None, used_aliases=None):
        """prepare JOIN statement recursively for all related tables"""
        # Set defaults for the root call.
        if current_alias is None:
            current_alias = table
        if used_aliases is None:
            used_aliases = {}
            
        data = {
            'join_string': '',
            'column_names': []
        }
        
        # Get and prefix column names with the current alias.
        data['column_names'].extend([f"{current_alias}.{col}" for col in self.get_column_names(table)])
        
        fk_list = self.cursor.execute(f"PRAGMA foreign_key_list({table});").fetchall()
        if fk_list:
            for fk in fk_list:
                parent_table = fk[2]  # foreign table name
                # Determine the alias for the parent table.
                if parent_table in used_aliases:
                    used_aliases[parent_table] += 1
                    parent_alias = f"{parent_table}_{used_aliases[parent_table]}"
                else:
                    used_aliases[parent_table] = 0  # first occurrence, use table name directly
                    parent_alias = parent_table
                    
                # Build the join clause using the appropriate alias.
                join_clause = f" LEFT JOIN {parent_table}"
                if parent_alias != parent_table:
                    join_clause += f" AS {parent_alias}"
                join_clause += f" ON {parent_alias}.{fk[4]} = {current_alias}.{fk[3]}"
                data['join_string'] += join_clause
                
                # Recursively add join strings from the parent table.
                child_data = self.add_join_string(parent_table, current_alias=parent_alias, used_aliases=used_aliases)
                data['join_string'] += child_data['join_string']
                data['column_names'].extend(child_data['column_names'])
                
        return data
    
    def get_all_related_data(self, table, limit=100):
        data = self.add_join_string(table)
        #filter non id columns
        filtered = [col for col in data['column_names'] if 'id' not in col]
        query = f'SELECT {",".join(filtered)} FROM {table}'

        query += data['join_string']
        query += f' LIMIT {limit}'
        self.cursor.execute(query)
        return pandas.DataFrame(self.cursor.fetchall(), columns=filtered).to_string()

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