from db_handler import Db_handler
from data import tables, uk_regions
db = Db_handler("charity.db")

for key, value in tables.items():
    db.create_table(key, value)
    print(key, 'created')

for i, key in enumerate(uk_regions):
    db.insert_row('region', (key,))
    for city in uk_regions.get(key):
        db.insert_row('city', (city, i+1))
