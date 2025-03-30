tables = {
    "organization" : """
        organization_id INTEGER PRIMARY KEY AUTOINCREMENT,
        organization_name TEXT NOT NULL,
        postcode TEXT NOT NULL,
        contact_person TEXT NOT NULL
    """,
    "donor" : """
        donor_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        phone_number TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        donor_type TEXT NOT NULL,
        organization_id INTEGER,
        FOREIGN KEY(organization_id)
            REFERENCES organization(organization_id)
    """,
    "project" : """
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT NOT NULL,
        amount_goal REAL NOT NULL
    """,
    "objective" : """
        objective_id INTEGER PRIMARY KEY AUTOINCREMENT,
        objective_name TEXT NOT NULL,
        cost REAL,
        description TEXT
    """,
    "event" : """
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT,
        location_postcode TEXT,
        event_cost REAL,
        start_date_time TEXT,
        end_date_time TEXT,
        project_id INTEGER,
        FOREIGN KEY (project_id)
            REFERENCES project(project_id)
    """,
    "donation" : """
        donation_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        source TEXT NOT NULL,
        notes TEXT,
        donor_id INTEGER,
        event_id INTEGER,
        FOREIGN KEY (donor_id)
            REFERENCES donor(donor_ID)
                ON UPDATE RESTRICT
                ON DELETE RESTRICT,
        FOREIGN KEY (event_id)
            REFERENCES event(event_id)
    """,
    "project_objectives" : """
        project_and_objective_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        objective_id INTEGER,
        FOREIGN KEY (project_id)
            REFERENCES project(project_id),
        FOREIGN KEY (objective_id)
            REFERENCES objective(objective_id)
    """,
    "donation_allocation" : """
        donation_allocation_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        allocation_amount REAL NOT NULL,
        project_and_objective_id INTEGER,
        donation_Id INTEGER,
        FOREIGN KEY (project_and_objective_id)
            REFERENCES project_objectives(project_and_objective_id),    
        FOREIGN KEY (donation_Id)
            REFERENCES donation(donation_ID)
    """,
    "donor_details" : """
        donor_details_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        postcode TEXT NOT NULL,
        house_no INTEGER,
        donor_id INTEGER,
        FOREIGN KEY(donor_id)
            REFERENCES donor(donor_ID)
    """,
}