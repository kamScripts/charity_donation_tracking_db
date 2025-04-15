import random
import math
from db_handler import Db_handler
from data import tables, uk_regions
from populate_small_table import sample_data as small_table
from populate_db import db_data as large_table
from app_interface import main

db = Db_handler("charity.db")
db2 = Db_handler("small_table.db")

def create_db_and_fill(database: Db_handler ,create_statements,region_obj , table_data):
    """Create tables and insert mock data"""
    add_data = input('Do you want to create new database (y / n) ?')
    if add_data.lower() == 'y':  
        for key, value in create_statements.items():
            database.create_table(key, value)
            print(key, 'created')
        
    add_data = input('Do you want to add test data (y / n) ?')
    if add_data.lower() == 'y':
        region_names =map(lambda x: (x,), list(region_obj.keys()))

        database.insert_many('region', region_names)
        for i, key in enumerate(region_obj):
            for city in region_obj.get(key):
                database.insert_row_all_columns('city', (city, i+1))
        for key, value in table_data.items():
            database.insert_many(key, value)
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
        print('donations allocated')


#create_db_and_fill(db, tables, uk_regions, large_table)


db.print_result(db.get_all('donor', 'donor_id', (1,)))



#if __name__ == "__main__":
#    main(db)
   