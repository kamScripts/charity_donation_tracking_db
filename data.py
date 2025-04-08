tables = {
    "donation" : """
        donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        source TEXT NOT NULL,
        donation_date TEXT NOT NULL,
        notes TEXT,
        donor_id INTEGER,
        event_id INTEGER,
        FOREIGN KEY(donor_id)
        REFERENCES donor(donor_id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
        FOREIGN KEY(event_id)
        REFERENCES event(event_id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
    """,
    "region" : """
        region_id INTEGER PRIMARY KEY AUTOINCREMENT,
        region_name TEXT NOT NULL UNIQUE
    """,

    "city" : """
        city_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_name TEXT NOT NULL,
        region_id INTEGER NOT NULL,
        UNIQUE(city_name, region_id),
        FOREIGN KEY(region_id)
        REFERENCES region(region_id)
    """,
    
    "location" : """
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        street TEXT NOT NULL,
        building_no TEXT,
        postcode TEXT NOT NULL,
        city_id INTEGER NOT NULL,
        FOREIGN KEY(city_id)
        REFERENCES city(city_id)
    """,

    "donor" : """
        donor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        phone_number TEXT UNIQUE,
        email TEXT UNIQUE,
        location_id INTEGER,
        organization_name TEXT,
        FOREIGN KEY(location_id)
        REFERENCES location(location_id)
    """,
    
    "project" : """
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT NOT NULL,
        amount_goal REAL NOT NULL
    """,
    
    "objective" : """
        objective_id INTEGER PRIMARY KEY AUTOINCREMENT,
        objective_name TEXT NOT NULL,
        description TEXT,
        project_id INTEGER,
        FOREIGN KEY(project_id)
        REFERENCES project(project_id)
    """,
    
    "event" : """
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT NOT NULL,
        location_id INTEGER,
        event_cost REAL,
        event_date TEXT NOT NULL,
        project_id INTEGER,
        FOREIGN KEY(location_id)
        REFERENCES location(location_id),
        FOREIGN KEY(project_id)
        REFERENCES project(project_id)
    """,

    "donation_allocation" : """
        donation_allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        allocation_amount REAL NOT NULL,
        donation_id INTEGER,
        objective_id INTEGER,
        FOREIGN KEY(donation_id)
        REFERENCES donation(donation_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY(objective_id)
        REFERENCES objective(objective_id)
    """
}
uk_regions = {
    "North East": ["Newcastle upon Tyne", "Sunderland", "Durham"],
    "North West": ["Manchester", "Liverpool", "Preston"],
    "Yorkshire and the Humber": ["Leeds", "Sheffield", "Hull"],
    "East Midlands": ["Nottingham", "Leicester", "Derby"],
    "West Midlands": ["Birmingham", "Coventry", "Wolverhampton"],
    "East of England": ["Norwich", "Cambridge", "Luton"],
    "London": ["Westminster", "Camden", "Greenwich"],
    "South East": ["Brighton", "Oxford", "Southampton"],
    "South West": ["Bristol", "Plymouth", "Exeter"],
    "Scotland": ["Edinburgh", "Glasgow", "Aberdeen"],
    "Wales": ["Cardiff", "Swansea", "Newport"],
    "Northern Ireland": ["Belfast", "Londonderry", "Newry"]
}

