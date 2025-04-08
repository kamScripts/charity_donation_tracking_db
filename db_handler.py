import sqlite3
try:
    import pandas
except ModuleNotFoundError as e:
    print(e)
    
from db_basic import Db_basic

class Db_handler(Db_basic):
    DONATION_BY_DONOR = """
        SELECT donation_date, donation_id, amount, source, donation.donor_id,
        event_name, project_name FROM donation
        """

        
    def __init__(self, db_path):
        super().__init__(db_path)


    def get_by_column_value(self, table, column, value, opSign='='):
        """view records based on one condition."""

        query = f'SELECT * FROM {table} WHERE {column} {opSign} ?;'
        return self.read_query(query, (value,))
    
    def get_all_events_donations_summary(self):
        """get all events summary of all events"""

        data = self.add_join_clause('donation')
        query = """
        SELECT donation.event_id, event_name, event_date, project_name, location.postcode,
        event_cost, SUM(amount) AS donations_collected,
        COUNT(donation_ID) AS number_of_donations,
        MAX(amount) AS Highest_donation, AVG(amount) AS Average_donation
        FROM donation
        """
        query += data['join_string']
        query +="""
        GROUP BY donation.event_id HAVING event_name NOT Null
        ORDER BY event_date DESC
        ;"""
        return self.read_query(query)

    def get_event_donations_summary(self, event_id):
        """get summary of single event"""
        
        data = self.add_join_clause('donation')
        query = """
        SELECT donation.event_id, event_name, event_date, project_name, location.postcode,
        event_cost, SUM(amount) AS donations_collected,
        COUNT(donation_ID) AS number_of_donations,
        MAX(amount) AS Highest_donation, AVG(amount) AS Average_donation
        FROM donation
        """
        query += data['join_string']
        query +=' GROUP BY donation.event_id HAVING donation.event_id=?;'
        return self.read_query(query, (event_id,))

    def get_total_donations_by_all_donors(self):
        """get summary of all donation grouped by donor_id"""

        query = """
        SELECT donation.donor_id, first_name, last_name, organization_name,
        SUM(amount) AS total_donations,
        AVG(amount) AS average_donation,
        COUNT(donation_id) AS number_of_donations
        FROM donation 
        LEFT JOIN donor ON donation.donor_id=donor.donor_id 
        GROUP BY donor.donor_id 
        ;"""
        return self.read_query(query)
    
    def get_total_donations_by_donor_name(self, name):
        """get summary of donor's donations"""
        
        first_name, last_name = name.split(' ')
        query = """
        SELECT donation.donor_id, first_name, last_name, organization_name,
        SUM(amount) AS total_donations,
        AVG(amount) AS average_donation,
        COUNT(donation_id) AS number_of_donations
        FROM donation 
        LEFT JOIN donor ON donation.donor_id=donor.donor_id 
        GROUP BY donor.donor_id
        HAVING first_name = ?
        AND last_name = ? 
        ;"""
        return self.read_query(query, (first_name.capitalize(), last_name.capitalize()))

    def get_donations_by_donor_name(self, name):
        """Find all donations for a donor name"""

        first_name, last_name = name.split(' ')
        data = self.add_join_clause('donation')
        query = self.DONATION_BY_DONOR
        query+= data['join_string']
        query+= """
        WHERE donor.first_name = ? AND donor.last_name = ?
        ORDER BY donation_date DESC
        ;"""
        try:
            return pandas.read_sql_query(
                query, self.connection, params=[first_name.capitalize(), last_name.capitalize()])
        except NameError as e:
            print(e)
            return self.cursor.execute(query, (first_name.capitalize(), last_name.capitalize()))
    def get_donations_by_donor_id(self, id):
        """Find all donations for a donor id"""

        data = self.add_join_clause('donation')
        query = self.DONATION_BY_DONOR
        query+= data['join_string']
        query+= ' WHERE donor.donor_id = ? ORDER BY donation_date DESC;'
        return self.read_query(query, (id,))

    def check_donation_allocation(self, id):
        """Check on what donor's donations where spent."""
        data = self.add_join_clause('donation_allocation')
        query = """
        SELECT donation.donation_id AS donation_id, donation_date,
        amount AS donation_amount, allocation_amount,
        objective_name, project.project_name FROM donation_allocation 
        """
        query += data['join_string']
        query += ' WHERE donation.donor_id = ?'
        return self.read_query(query, (id,))

    def get_donor_by_name(self, name):
        """Search donor details by name"""
        first_name, last_name = name.split(' ')
        data = self.add_join_clause('donor')
        query = 'SELECT * FROM donor'
        query += data['join_string']
        query += ' WHERE first_name = ? AND last_name = ?'
        return self.read_query(query, (first_name.capitalize(), last_name.capitalize()))
    def get_all_donors(self, donor_type:str): 
        """Return donors by type i for individual, o for organization"""       
        donors = self.get_all('donor')
        try:
            individual = donors.loc[:, donors.columns!='organization_name']
            organizational = self.get_all('donor')[donors['organization_name'].notna()]
        except AttributeError as e:
            print(e)
            individual = organizational = donors
            
        
        if donor_type == 'i':
            return individual
        if donor_type == 'o':
            return organizational
        
        
    def insert_row_all_columns(self, table, values: tuple):
        """Insert single records if all rows are not empty."""
        #slice column names to ommit id column
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