from db_handler import Db_handler
from data import tables, uk_regions
from populate_small_table import sample_data
#from populate_db import (individual_donors,
#organization_donors,location_data, donations, projects, objectives, events)


db = Db_handler("charity.db")

for key, value in tables.items():
    db.create_table(key, value)
    print(key, 'created')
##populate region and city tables
#for i, key in enumerate(uk_regions):
#    db.insert_row_all_columns('region', (key,))
#    for city in uk_regions.get(key):
#        db.insert_row_all_columns('city', (city, i+1))
#db.insert_many('project', projects)
#db.insert_many('objective', objectives)
#db.insert_many('event', events)
#db.insert_many('location', location_data)
#db.insert_many('donor', individual_donors)
#db.insert_many('donor', organization_donors)
#db.insert_many('donation', donations)
#print(db.get_table_names())
#print(db.get_by_id('donor', 1))
#print(db.get_by_column_value('donor', 'first_name', 'Jasmine'))
#print(db.get_all_related_data('donor'))
#print(db.get_by_column_value('donation', 'donor_id', 81))
#print(db.get_total_donations_by_id(1))


for key, value in sample_data.items():    
    if key == 'region':
        db.insert_row_all_columns('region', sample_data['region'][0])
    else:
        db.insert_many(key, value)
print(db.get_total_donations_by_id())
print(db.get_donor_info())
print(db.get_all('event'))