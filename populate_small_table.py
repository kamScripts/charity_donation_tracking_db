sample_data = {
    "region": [
        ("Western Region",)
    ],
    
    "city": [
        ("Oakville", 1),
        ("Riverdale", 1)
    ],
    
    "location": [
        ("Maple Avenue", "123", "12345", 1),
        ("Oak Street", "456", "12346", 1),
        ("Pine Road", "789", "12347", 2),
        ("Cedar Boulevard", "101", "12348", 2),
        ("Elm Street", "202", "12349", 1),
        ("Community Center Road", "500", "12345", 1),
        ("Town Hall Plaza", "1", "12347", 2)
    ],
    
    "donor": [
        ("John", "Smith", "555-123-4567", "john.smith@email.com", 1, None),
        ("Jane", "Doe", "555-234-5678", "jane.doe@email.com", 2, None),
        ("Robert", "Johnson", "555-345-6789", "robert.johnson@email.com", 3, None),
        ("Sarah", "Williams", "555-456-7890", "sarah.williams@email.com", 4, None),
        (None, None, "555-567-8901", "contact@acmecorp.com", 5, "ACME Corporation")
    ],
    
    "project": [
        ("Community Garden Initiative", 50000.00)
    ],
    
    "objective": [
        ("Garden Construction", "Building raised beds and irrigation systems", 1),
        ("Educational Programs", "Developing gardening workshops and school programs", 1)
    ],
    
    "event": [
        ("Spring Fundraising Gala", 6, 5000.00, "2025-04-15", 1),
        ("Summer Garden Party", 7, 3000.00, "2025-07-20", 1)
    ],
    
    "donation": [
        # John Smith's donations (5)
        (500.00, "Credit Card", "2025-01-10", "Monthly supporter", 1, None),
        (500.00, "Credit Card", "2025-02-10", "Monthly supporter", 1, None),
        (1000.00, "Check", "2025-04-15", "At gala event", 1, 1),
        (750.00, "Mobile App", "2025-07-20", "Summer event donation", 1, 2),
        
        # Jane Doe's donations (5)
        (250.00, "PayPal", "2025-01-15", None, 2, None),
        (250.00, "PayPal", "2025-03-15", None, 2, None),
        (1500.00, "Check", "2025-04-15", "Gala major donor", 2, 1),
        (250.00, "PayPal", "2025-06-15", None, 2, None),
        (500.00, "Mobile App", "2025-07-20", "Summer event", 2, 2),
        
        # Robert Johnson's donations (5)
        (100.00, "Website", "2025-01-20", "First-time donor", 3, None),
        (100.00, "Website", "2025-03-22", None, 3, None),
        (750.00, "Credit Card", "2025-04-15", "Gala attendance", 3, 1),
        (100.00, "Website", "2025-06-22", None, 3, None),
        (300.00, "Cash", "2025-07-20", "Summer event donation", 3, 2),
        
        # Sarah Williams's donations (5)
        (1000.00, "Bank Transfer", "2025-01-05", "Quarterly donation", 4, None),
        (200.00, "PayPal", "2025-03-15", "Extra contribution", 4, None),
        (2000.00, "Check", "2025-04-15", "VIP Gala sponsor", 4, 1),
        (1000.00, "Bank Transfer", "2025-07-05", "Quarterly donation", 4, None),
        (1000.00, "Credit Card", "2025-07-20", "Summer event sponsor", 4, 2),
        
        # ACME Corporation's donations (5)
        (5000.00, "Corporate Check", "2025-01-15", "Corporate sponsor", 5, None),
        (500.00, "Electronic Transfer", "2025-03-15", "Monthly corporate gift", 5, None),
        (10000.00, "Corporate Check", "2025-04-15", "Gala platinum sponsor", 5, 1),
        (500.00, "Electronic Transfer", "2025-06-15", "Monthly corporate gift", 5, None),
        (7500.00, "Corporate Check", "2025-07-20", "Summer event main sponsor", 5, 2)
    ],
    
    "donation_allocation": [
        # Allocations for John Smith's donations
        (300.00, 1, 1),
        (200.00, 1, 2),
        (300.00, 2, 1),
        (200.00, 2, 2),
        (600.00, 3, 1),
        (400.00, 3, 2),
        (300.00, 4, 1),
        (200.00, 4, 2),
        (450.00, 5, 1),
        (300.00, 5, 2),
        
        # Allocations for Jane Doe's donations
        (150.00, 6, 1),
        (100.00, 6, 2),
        (150.00, 7, 1),
        (100.00, 7, 2),
        (900.00, 8, 1),
        (600.00, 8, 2),
        (150.00, 9, 1),
        (100.00, 9, 2),
        (300.00, 10, 1),
        (200.00, 10, 2),
        
        # Allocations for Robert Johnson's donations
        (60.00, 11, 1),
        (40.00, 11, 2),
        (60.00, 12, 1),
        (40.00, 12, 2),
        (450.00, 13, 1),
        (300.00, 13, 2),
        (60.00, 14, 1),
        (40.00, 14, 2),
        (180.00, 15, 1),
        (120.00, 15, 2),
        
        # Allocations for Sarah Williams's donations
        (600.00, 16, 1),
        (400.00, 16, 2),
        (120.00, 17, 1),
        (80.00, 17, 2),
        (1200.00, 18, 1),
        (800.00, 18, 2),
        (600.00, 19, 1),
        (400.00, 19, 2),
        (600.00, 20, 1),
        (400.00, 20, 2),
        
        # Allocations for ACME Corporation's donations
        (3000.00, 21, 1),
        (2000.00, 21, 2),
        (300.00, 22, 1),
        (200.00, 22, 2),
        (6000.00, 23, 1),
        (4000.00, 23, 2),
        (300.00, 24, 1),
        (200.00, 24, 2),
        (4500.00, 25, 1),
        (3000.00, 25, 2)
    ]
}