from db_handler import Db_handler
from data import tables, uk_regions, projects, objectives, events
from populate_db import individual_donors, organization_donors,location_data

db = Db_handler("charity.db")

for key, value in tables.items():
    db.create_table(key, value)
    print(key, 'created')
#populate region and city tables
for i, key in enumerate(uk_regions):
    db.insert_row('region', (key,))
    for city in uk_regions.get(key):
        db.insert_row('city', (city, i+1))
db.insert_many('project', projects)
db.insert_many('objective', objectives)
db.insert_many('event', events)
db.insert_many('location', location_data)
db.insert_many('donor', individual_donors)
db.insert_many('donor', organization_donors)
