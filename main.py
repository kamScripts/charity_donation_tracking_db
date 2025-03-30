from db_handler import Db_handler
from data import tables
db = Db_handler("charity.db")

for key, value in tables.items():
    db.create_table(key, value)
    print(key, 'created')
