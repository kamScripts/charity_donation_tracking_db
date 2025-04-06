import sqlite3
import pandas
class Db_basic:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.connection.execute("PRAGMA foreign_keys = ON")
    

    def drop_table(self, table): 
              
        self.cursor.execute(f'DROP TABLE IF EXISTS {table}')
        
    def create_table(self, table, values):
        self.connection.execute("PRAGMA foreign_keys = OFF")
        self.drop_table(table)
        query = f'CREATE TABLE {table} ({values});'
        self.cursor.execute(query)
        self.connection.commit()
        self.connection.execute("PRAGMA foreign_keys = ON")
    def query_table_all(self, query, params):
        """Query table with parameters, fetch all results"""
        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        return results

    def query_table_one(self, query, params):
        """Query table with parameters, fetch all results"""
        self.cursor.execute(query, params)
        results = self.cursor.fetchone()
        return results

    def insert_row(self, table, columns: list, values: tuple):
        """Insert a single record."""
        placeholders = ', '.join(['?' for _ in enumerate(columns)])
        query = f'INSERT INTO {table}({", ".join(columns)}) VALUES({placeholders})'
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print(f'{values} inserted successfully into {table}')
        except sqlite3.OperationalError as e:
            print(e)
        except sqlite3.IntegrityError as e:
            print(e)
        
    def insert_many_rows(self, table, columns: list, values: list):
        """Insert list of the records."""
        placeholders = ', '.join(['?' for _ in enumerate(columns)])
        query = f'INSERT INTO {table}({", ".join(columns)}) VALUES({placeholders})'
        try:
            self.cursor.executemany(query, values)
            self.connection.commit()
            print(f'dataset inserted successfully into {table}')
        except sqlite3.OperationalError as e:
            print(e)
        except sqlite3.IntegrityError as e:
            print(e,f' while inserting into {table}')
    
    def get_table_names(self):
        """return all table names in the database."""
        results = self.cursor.execute('SELECT DISTINCT tbl_name FROM sqlite_schema WHERE tbl_name != "sqlite_sequence";')        
        return results.fetchall()

    def get_column_names(self, table):
        """return all column names in the table"""
        table_info = self.cursor.execute(f'PRAGMA table_info({table})')
        #use slicing to remove ID column
        return [column[1] for column in table_info.fetchall()]
    
    def get_by_id(self, table, id):
        """get record by ID"""
        query = f'SELECT * FROM {table} WHERE {table}_id = ?;'
        
        
        try:
            data=pandas.read_sql_query(query, self.connection, params=[id])
        except ImportError as e:
            self.cursor.execute(query, (id,))
            data = self.cursor.fetchall()
            print(e)

        return data
    def __add_join_string(self, table, current_alias=None, used_aliases=None):
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
                child_data = self.__add_join_string(parent_table, current_alias=parent_alias, used_aliases=used_aliases)
                data['join_string'] += child_data['join_string']
                data['column_names'].extend(child_data['column_names'])

        return data

    def __get_all_related_data(self, table):
        """get all related tables"""
        data = self.__add_join_string(table)        
        filtered = [col for col in data['column_names'] if 'id' not in col ] 
        query = f'SELECT {",".join(filtered)} FROM {table}'
        query += data['join_string']
        
        try:
            return pandas.read_sql_query(query, self.connection)
        except ImportError:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        
    def add_join_clause(self, table):
        return self.__add_join_string(table)
    def get_all(self,table):
        return self.__get_all_related_data(table)
    
    def delete_record(self, table, record_id):
        row_to_delete = self.get_by_id(table, record_id)
        self.cursor.execute(f'DELETE FROM {table} WHERE {table}_id = ?', (record_id,))
        self.connection.commit()
        print( row_to_delete, ' removed from the table')
        
    
    