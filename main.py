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

create_db_and_fill(db, tables, uk_regions, large_table)
create_db_and_fill(db2, tables, uk_regions, small_table)

print(db.get_total_donations_by_all_donors())
print(db.get_all_donors_info())
print(db.get_donor_by_name('denise carroll'))


print(db.check_donation_allocation(5))
print(db.get_all('event'))
print(db.get_donations_by_donor_name('billy chapman'))
print(db.get_by_column_value('project', 'project_name', 'Community Garden Initiative'))
print(db.get_column_names('donor'))

db.update_records('donor', 5, ['first_name', 'last_name'], ('Kamil', 'Gebski'))
print(db.get_event_donations_summary(1))
print(db.get_all_events_donations_summary())
print(db.get_by_id('donor', 1))
print(db.get_total_donations_by_donor_name('kamil gebski'))
print(db.get_donations_by_donor_id(5))
print(db.get_donor_by_name('kamil gebski'))
