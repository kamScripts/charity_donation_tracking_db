import random
import math
from db_handler import Db_handler
from data import tables, uk_regions
from populate_small_table import sample_data as small_table
from populate_db import db_data as large_table


db = Db_handler("charity.db")
db2 = Db_handler("small_table.db")


def create_db_and_fill(database: Db_handler ,create_statements,region_obj , table_data):
    """Create tables and insert data"""
    for key, value in create_statements.items():
        database.create_table(key, value)
        print(key, 'created')
    region_names =map(lambda x: (x,), list(region_obj.keys()))

    database.insert_many('region', region_names)
    for i, key in enumerate(region_obj):
        for city in region_obj.get(key):
            database.insert_row_all_columns('city', (city, i+1))
    for key, value in table_data.items():
        database.insert_many(key, value)
def add_donation_allocation(database: Db_handler):
    """Allocate donations to the project's objectives"""
    last_donation =  database.get_last_row('donation')[0]
    last_objective = database.get_last_row('objective')[0]
    allocations = []
    randoms = []
    for _ in range(math.floor(last_donation / 2)):
        rand = random.randint(1, last_donation)        
        if rand not in randoms:
            donation =  database.query_table_one(
                'SELECT * FROM donation WHERE donation_id = ?',
                (rand,))
            randoms.append(randoms)
            allocations.append((donation[1], donation[0], random.randint(1, last_objective)))
        else:
            continue
        
    
    db.insert_many('donation_allocation', allocations)
    db.print_result('donations allocated')


create_db_and_fill(db, tables, uk_regions, large_table)
create_db_and_fill(db2, tables, uk_regions, small_table)
add_donation_allocation(db)
db.print_result(db.get_total_donations_by_all_donors())
db.print_result(db.check_donation_allocation(900))
db.print_result(db.get_donations_by_donor_name('billy chapman'))
db.print_result(db.get_by_column_value('project', 'project_name', 'Community Garden Initiative'))
db.print_result(db.get_column_names('donor'))
db.update_records('donor', 5, ['first_name', 'last_name'], ('Kamil', 'Gebski'))
db.print_result(db.get_event_donations_summary(1))
db.print_result(db.get_all_events_donations_summary())
db.print_result(db.get_total_donations_by_donor_name('kamil gebski'))
db.print_result(db.get_donations_by_donor_id(5))
db.print_result(db.get_donor_by_name('kamil gebski'))
db.print_result((db.get_by_id('donor', 5)))
db.print_result(db.get_all_donors('i'))