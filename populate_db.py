from data import uk_regions
from faker import Faker
import random

fake = Faker('en_GB')
source = ['regular', 'one-time', 'event']

# Charity Event Name Generator Words
action_words = [
    "Run", "Walk", "Ride", "Climb", "Swim", "Dance", "Gala", "Festival",
    "Auction", "Marathon", "Challenge", "Fundraiser", "Celebration"
]

charity_words = [
    "Hope", "Love", "Kindness", "Giving", "Caring", "Support", "Change",
    "Impact", "Dream", "Inspire", "Compassion"
]

seasonal_words = [
    "Spring", "Summer", "Winter", "Holiday", "Christmas", "Thanksgiving", "Autumn"
]

project_actions = [
    "Build", "Restore", "Create", "Empower", "Grow", "Sustain", "Improve",
    "Develop", "Transform"
]

beneficiaries = [
    "Community", "Future", "Generations", "Families", "Children", "Students",
    "Seniors", "Animals", "Environment"
]

cause_specific_words = [
    "Shelter", "Education", "Water", "Health", "Food", "Technology", "Arts", "Green"
]

# Function to generate a random charity event name
def generate_event_name():
    return f"{random.choice(seasonal_words)} {random.choice(action_words)} for {random.choice(charity_words)}"

# Function to generate a random charity project name
def generate_project_name():
    return f"{random.choice(project_actions)} {random.choice(beneficiaries)} {fake.year()}"
def generate_objective_name():
    return f"{random.choice(project_actions)} {random.choice(cause_specific_words)} for {random.choice(beneficiaries)}"

try:
    location_data = [(fake.street_name(), fake.random_int(min=1, max=200),
                    fake.postcode(), fake.random_int(min=1, max=36)) for _ in range(1100)]
    individual_donors = [(fake.first_name(), fake.last_name(), fake.phone_number(),f'{fake.random_int(min=2, max=49) * fake.random_digit()}{fake.email()}', fake.random_int(min=1, max=900), None) for _ in range(890)]
    organization_donors = [(fake.first_name(), fake.last_name(), fake.phone_number(), fake.company_email(), 901 + num, fake.company()) for num in range(100)]

    donations = [(float(fake.random_int(min=5, max=1000, step=5)), source[fake.random_int(min=0, max=2)], fake.date_between(start_date='-5y'),
                fake.text(max_nb_chars=100, ext_word_list=['Ucen', 'Manchester', 'database', '3NF', '2NF', 'PK', 'FK', 'composite key' ]),
                fake.random_int(min=1, max=500), None
                ) for _ in range(5000)]
    def setEventFk(tupl):
        if tupl[1] == 'event':
            temp = tupl
            tupl = (temp[0], temp[1], temp[2], temp[3], temp[4], fake.random_int(min=1, max=20))
            return tupl
        else:
            return tupl
    donations = [setEventFk(donation) for donation in donations]
    projects = [(generate_project_name(), fake.random_int(min=100000, max=500000, step=50000)) for _ in range(10)]
    events = [(generate_event_name(), fake.random_int(min=1001, max=1100), fake.random_int(min=5000, max=10000),
            fake.date_between(start_date='-5y'), fake.random_int(min=1, max=10)) for _ in range(40)]
    objectives = [(generate_objective_name(),
                fake.text(max_nb_chars=100,
                            ext_word_list=['Ucen', 'Manchester', 'database', '3NF', '2NF', 'PK', 'FK', 'composite key' ]),
                    fake.random_int(min=1, max=10)
                ) for _ in range(50)]
    db_data = {
        'project': projects,
        'objective': objectives,
        
    }
except ImportError as e:
    print(e)