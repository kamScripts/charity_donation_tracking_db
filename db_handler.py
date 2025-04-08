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
    def get_event_donations_summary(self, event_id):
        """get summary of all events"""
        data = self.add_join_clause('donation')
        
        query = """
        SELECT donation.event_id, event_name, event_date, project_name, location.postcode,
        event_cost, SUM(amount) AS donations_collected, COUNT(donation_ID) AS number_of_donations,
        MAX(amount) AS Highest_donation, AVG(amount) AS Average_donation
        FROM donation """
        
        query += data['join_string']
        query +=' GROUP BY donation.event_id HAVING donation.event_id=?'
        
        try:
            tb = pandas.read_sql_query(query, self.connection, params=[event_id])
            return tb.to_string()
        except ImportError as e:
            print(e)
            self.cursor.execute(query)
            return self.cursor.fetchall()
    def get_total_donations_by_donors(self):
        """get summary of all donation grouped by donor_id"""
        query = """
        SELECT donation.donor_id, first_name, last_name, organization_name, SUM(amount) AS total_donations,
        AVG(amount) AS average_donation, COUNT(donation_id) AS number_of_donations
        FROM donation 
        LEFT JOIN donor ON donation.donor_id=donor.donor_id 
        GROUP BY donation.donor_id 
        ;"""

        try:
            tb = pandas.read_sql_query(query, self.connection)
            return tb.to_string()
        except ImportError as e:
            print(e)
            self.cursor.execute(query)
            return self.cursor.fetchall()
    def get_donations_by_donor_name(self, name):
        """Find all donations for a donor name"""
        
        first_name, last_name = name.split(' ')
        data = self.add_join_clause('donation')
        query = 'SELECT donation_date, donation_id, amount, source, donation.donor_id, event_name, project_name FROM donation'
        query+= data['join_string']
        query+= ' WHERE donor.first_name = ? AND donor.last_name = ? ORDER BY donation_date DESC'
        return pandas.read_sql_query(
            query, self.connection, params=[first_name.capitalize(), last_name.capitalize()])
    
    def get_donations_by_donor_id(self, id):
        """Find all donations for a donor id"""
        
        data = self.add_join_clause('donation')
        query = 'SELECT donation_date, donation_id, amount, source, event_name, project_name FROM donation'
        query+= data['join_string']
        query+= ' WHERE donor.donor_id = ? ORDER BY donation_date DESC'
        return pandas.read_sql_query(query, self.connection, params=[id])
    
    def check_donation_allocation(self, id):
        """Check on what donor's donations where spent."""
        data = self.add_join_clause('donation_allocation')
        query = """
        SELECT donation.donation_id AS donation_id, donation_date, amount AS donation_amount, allocation_amount,
        objective_name, project.project_name FROM donation_allocation """
        query += data['join_string']
        query += ' WHERE donation.donor_id = ?'
        return pandas.read_sql_query(query, self.connection, params=[id])
    def get_all_donors_info(self):
        """Return all donors information"""
        tbl = self.get_all('donor')
        
        try:
            tbl.to_string()
        except ImportError as e:
            print(e)
        return tbl
    
    def get_donor_by_name(self, name):
        """Search donor details by name"""
        first_name, last_name = name.split(' ')
        data = self.add_join_clause('donor')
        query = 'SELECT * FROM donor'
        query += data['join_string']
        query += ' WHERE first_name = ? AND last_name = ?'
        try:
            return pandas.read_sql_query(
                query, self.connection, params=[first_name.capitalize(), last_name.capitalize()]).to_string()
        except ImportError:
            self.cursor.execute(query, (first_name.capitalize(), last_name.capitalize()))
            return self.cursor.fetchall()
    
    def insert_row_all_columns(self, table, values: tuple):
        """Insert single records if all rows are not empty."""
        columns = self.get_column_names(table)[1:]
        placeholders = ', '.join(['?' for _ in enumerate(columns)])
        query = f'INSERT INTO {table}({", ".join(columns)}) VALUES({placeholders});'
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print(f'{values} inserted successfully into {table}')
        except sqlite3.OperationalError as e:
            print(e)
        except sqlite3.IntegrityError as e:
            print(e)
        
    def insert_many(self, table, data):
        """insert many records when all rows are not empty"""
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