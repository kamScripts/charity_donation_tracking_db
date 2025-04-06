from db_handler import Db_handler
from data import tables, uk_regions
from populate_small_table import sample_data
#from populate_db import (individual_donors,
#organization_donors,location_data, donations, projects, objectives, events)


db = Db_handler("charity.db")

#for key, value in tables.items():    
#    db.create_table(key, value)
#    print(key, 'created')
#populate region and city tables
#for i, key in enumerate(uk_regions):
#    db.insert_row_all_columns('region', (key,))
#    for city in uk_regions.get(key):
#        db.insert_row_all_columns('city', (city, i+1))
#db.insert_many('project', projects)
#db.insert_many('objective', objectives)
#db.insert_many('location', location_data)
#db.insert_many('donor', individual_donors)
#db.insert_many('donor', organization_donors)
#db.insert_many('event', events)
#db.insert_many('donation', donations)

#for key, value in sample_data.items():
#    if key == 'region':
#        db.insert_row_all_columns('region', sample_data['region'][0])
#    else:
#        db.insert_many(key, value)
#print(db.get_total_donations_by_donors())
#print(db.get_all_donors_info().to_string())
#print(db.get_donor_by_name('Jane Doe'))

#print(db.get_donations_by_donor_id(2))
#print(db.check_donation_allocation(5))
#print(db.get_all('event'))
#print(db.get_donations_by_donor_name('john smith'))
db.delete_event(1)
db.delete_record('event', 2)
