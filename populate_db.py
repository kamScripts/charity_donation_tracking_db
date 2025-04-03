from faker import Faker
import random

fake = Faker('en_GB')

location_data = [(fake.street_name(), fake.random_int(min=1, max=200),
                  fake.postcode(), fake.random_int(min=1, max=36)) for _ in range(500)]
individual_donors = [(fake.first_name(), fake.last_name(), fake.phone_number(), fake.email(), fake.random_int(min=1, max=490), None) for _ in range(490)]
organization_donors = [(fake.first_name(), fake.last_name(), fake.phone_number(), fake.email(), 491 + num, fake.company()) for num in range(10)]
print(organization_donors)
print(individual_donors)
