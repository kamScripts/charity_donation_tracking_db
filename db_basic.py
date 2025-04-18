import sqlite3
import re
try:
    import pandas
except ModuleNotFoundError as e:
    print(e)
class Db_basic:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.connection.execute("PRAGMA foreign_keys = ON")

    def drop_table(self, table):
        """Delete a table"""      
        self.cursor.execute(f'DROP TABLE IF EXISTS {table}')

    def create_table(self, table, values):
        """Create a table"""
        #  Foreign key constraints are turned off for the process of creating a table.
        self.connection.execute("PRAGMA foreign_keys = OFF")
        self.drop_table(table)
        query = f'CREATE TABLE {table} ({values});'
        self.cursor.execute(query)
        self.connection.commit()
        self.connection.execute("PRAGMA foreign_keys = ON")

    def query_table_all(self, query, params=None)->tuple:
        """Query table with parameters, fetch all results"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def query_table_one(self, query, params=None)->tuple:
        """Query table with parameters, fetch all results"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
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
            
    def get_last_row(self, table):
        """return last row of the table"""
        return self.query_table_one(f'SELECT * FROM {table} ORDER BY {table}_id DESC LIMIT 1;')

    def get_table_names(self):
        """return all table names in the database."""
        results = self.cursor.execute('SELECT DISTINCT tbl_name FROM sqlite_schema WHERE tbl_name != "sqlite_sequence";')
        return results.fetchall()

    def get_column_names(self, table):
        """return all column names in the table"""
        table_info = self.cursor.execute(f'PRAGMA table_info({table})')
        return [column[1] for column in table_info.fetchall()]

    def get_by_id(self, table, id):
        """get record  of any table by ID"""
        query = f'SELECT * FROM {table} WHERE {table}_id = ?;'
        return self.read_query(query, (id,))

    def __add_join_string(self, table, current_alias=None, used_aliases=None)->dict:
        """prepare JOIN statement recursively for all related tables"""
        # Set defaults for the initial call.
        # Aliases are used to avoid ambiguous column name error in a join statement.
        if current_alias is None:
            current_alias = table
        if used_aliases is None:
            used_aliases = {}
        # dictionary to store join statement and column names
        data = {
            'join_string': '',
            'column_names': []
        }
        # Get and prefix column names with the current alias.
        data['column_names'].extend(
            [f"{current_alias}.{col}" for col in self.get_column_names(table)]
            )
        # list of foreign keys related to the table
        fk_list = self.cursor.execute(f"PRAGMA foreign_key_list({table});").fetchall()
        if fk_list: # condition to end recursive call.
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
                child_data = self.__add_join_string(
                    parent_table, current_alias=parent_alias, used_aliases=used_aliases
                    )
                data['join_string'] += child_data['join_string']
                data['column_names'].extend(child_data['column_names'])
        return data

    def __get_all_related_data(self, table, col=None, param:tuple=None):
        """get all related tables"""
        data = self.__add_join_string(table)
        filtered = [col for col in data['column_names'] if 'id' not in col ]
        #add only child table id
        filtered.insert(0, data['column_names'][0])
        query = f'SELECT {",".join(filtered)} FROM {table}'
        query += data['join_string']
        if col:
            query += f' WHERE {col}= ?'
            return self.read_query(query, param)
        return self.read_query(query)

    def add_join_clause(self, table):
        """Call to a private method"""
        return self.__add_join_string(table)
    def get_all(self,table:str, col:str=None, optional_param:tuple=None):
        """Call a private method - get the child and parent tables data
        Col = column_name, param = column_value, for
        adding to query WHERE col = param"""

        return self.__get_all_related_data(table, col, optional_param)

    def delete_record(self, table, record_id):
        """delete row based on a record ID."""
        row_to_delete = self.get_by_id(table, record_id)
        try:
            self.cursor.execute(f'DELETE FROM {table} WHERE {table}_id = ?', (record_id,))
            self.connection.commit()
            print( row_to_delete, ' removed from the table')
        except sqlite3.Error as e:
            print(e)
    def delete_donor(self, donor_id):
        """Delete donations related with a donor then delete a donor."""
        self.cursor.execute('DELETE FROM donation WHERE donor_id = ?', (donor_id,))
        self.connection.commit()
        self.cursor.execute('DELETE FROM donor WHERE donor_id=?', (donor_id,))
        self.connection.commit()
        print('Donor and all related donations removed')
    def delete_event(self, event_id):
        """Delete donations related to the donor then delete a donor"""
        self.cursor.execute('DELETE FROM donation WHERE event_id = ?', (event_id,))
        self.connection.commit()
        self.cursor.execute('DELETE FROM event WHERE event_id=?', (event_id,))
        self.connection.commit()
        print('Event and all related donations removed')
    def update_records(self, table, id, fields: list, values: tuple):
        """Update records"""

        set_clause = ', '.join([f"{field} = ?" for field in fields])
        sql = f"UPDATE {table} SET {set_clause} WHERE {table}_id = ?"

        try:
            self.cursor.execute(sql, values + (id,))
            self.connection.commit()
            print('Record updated successfully:\n', self.get_by_id(table, id))
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
    def read_query(self, query:str, params:tuple=None):
        """Read query and return Pandas DataFrame or tuple if Pandas module
           not detected """
        #Extract table name from SELECT statement for case when pandas not installed
        try:
            #handle query with multi-line string
            query_one_line = query.replace('\n', ' ')
            col_match = re.search(r'SELECT\s+(.*?)\s+FROM', query_one_line, re.IGNORECASE)
            # Get the column part and split by commas
            columns_str = col_match.group(1)
            # Handle cases like "col1, col2 as alias, col3"
            columns = [col.strip().split(' AS ')[-1].strip() for col in columns_str.split(',')]
            # Remove any backticks or quotes from column names
            columns = [col.strip('`"\'') for col in columns]
        except (AttributeError, IndexError):
            columns = []
        if params:
            try:
                df = pandas.read_sql_query(query, self.connection, index_col=None,params=params)
                return df
            except NameError as e:
                print(e)
                self.cursor.execute(query, params)
                return (columns, self.cursor.fetchall())
        try:
            df = pandas.read_sql_query(query, self.connection)
            return df
        except (NameError, AttributeError)as e:
            print(e)


        self.cursor.execute(query)
        return (columns, self.cursor.fetchall())

    def print_result(self, result):
        try:
            # Try pandas DataFrame first
            results = result.to_string(index=False)
            print(results)
            return
        except (AttributeError, NameError) as e:
            print(e)
        
        if len(result[0]) <= 1:
            print(result[1])
        try:
            # Get column names and data
            if isinstance(result, tuple) and len(result) == 2:
                col_names = result[0]
                data = result[1]
                
                # If no data returned
                if not data:
                    print("No data found")
                    return
                
                # Calculate column widths based on column names and data
                col_widths = [len(str(name)) for name in col_names]
                
                for row in data:
                    for i, val in enumerate(row):
                        if i < len(col_widths):  # Ensure to don't go out of bounds
                            str_val = str(val)
                            # Update width if this value is longer
                            col_widths[i] = max(col_widths[i], len(str_val))
                
                # Generate header row with proper spacing
                header = " | ".join(str(name).center(col_widths[i]) for i, name in enumerate(col_names))
                separator = "-" * len(header)
                
                print(header)
                print(separator)
                
                # Print data rows with proper alignment
                for row in data:
                    row_str = " | ".join(str(val).center(col_widths[i]) for i, val in enumerate(row) if i < len(col_widths))
                    print(row_str)
            else:
                # Handle unexpected format
                print("Unexpected result format")
        except Exception as e:
            print(f"Error formatting results: {e}")
            # Fallback to simple output
            print(result)