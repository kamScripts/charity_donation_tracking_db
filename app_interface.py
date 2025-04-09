import sys
from db_handler import Db_handler
from populate_db import source
### add and check if args inside self.functions are correct

class DatabaseTerminalApp:
    def __init__(self, db: Db_handler):
        self.db = db
        self.running = True
        self.d_source = source
        self.main_menu = [
            "Donations Viewing",
            "Donors Viewing",
            "Event & Projects Viewing",
            "Database Management"
        ]
        self.category_functions = {
            0: [ # Donations
                {
                    "name": "Donations summary for all donors.",
                    "function": lambda: self.db.print_result(self.db.get_total_donations_by_all_donors()),
                    "args": []
                },
                            {
                    "name": "Donations summary by donor name.",
                    "function": lambda name: self.db.print_result(self.db.get_total_donations_by_donor_name(name)),
                    "args": [("Enter donor name: ", str)]
                },
                {
                    "name": "All donations, search by donor name",
                    "function": lambda name: self.db.print_result(self.db.get_donations_by_donor_name(name)),
                    "args": [("Enter donor name: ", str)]
                },
                {
                    "name": "All donations, search by donor ID",
                    "function": lambda donor_id: self.db.print_result(self.db.get_donations_by_donor_id(donor_id)),
                    "args": [("Enter donor ID: ", int)]
                },
                {
                    "name": "All donations, search by source",
                    "function": lambda value: self.db.print_result(self.db.get_by_column_value(
                        'donation', 'source', value, '=')),
                    "args": [(f"Enter source({', '.join(self.d_source)}): ", str)]
                },
                {
                    "name": "All donations, search by date",
                    "function": lambda value, op_sign: self.db.print_result(self.db.get_by_column_value(
                        'donation', 'donation_date', value, op_sign)),
                    "args": [("Enter date(Format: yyyy-mm-dd): ", str),
                             ("Before, Exact, or After, enter sign(<, =, >):", str)]
                },
                {
                    "name": "Single event donations summary",
                    "function": lambda event_id: self.db.print_result(self.db.get_event_donations_summary(event_id)),
                    "args": [("Enter event ID: ", int)]
                },
                {
                    "name": "All events donations summary",
                    "function": lambda: self.db.print_result(self.db.get_all_events_donations_summary()),
                    "args": []
                }
            ],
            1: [  # Donors
                {
                    "name": "All donors",
                    "function": lambda donor_type: self.db.print_result(self.db.get_all_donors(donor_type)),
                    "args": [("Enter (i) for Individual or (o) for organizations: ", str)]
                },
                {
                    "name": "View donors, search by Region",
                    "function": lambda reg: self.db.print_result(self.db.get_all('donor', 'region_name', (reg,))),
                    "args": [("Enter Region: ", str)]
                },
                {
                    "name": "View donors, search by City",
                    "function": lambda city: self.db.print_result(self.db.get_all('donor', 'city_name', (city,))),
                    "args": [("Enter City: ", str)]
                },
                
                {
                    "name": "View donor, search by name",
                    "function": lambda name: self.db.print_result(self.db.get_donor_by_name(name)),
                    "args": [("Enter donor name: ", str)]
                },
                {
                    "name": "View donor, search by ID",
                    "function": lambda id: self.db.print_result(self.db.get_all('donor', 'donor_id', (id,))),
                    "args": [("Enter donor ID: ", int)]
                },
                {
                    "name": "Check the donor's donations allocation.",
                    "function": lambda id: self.db.print_result(self.db.check_donation_allocation(id)),
                    "args": [("Some donation may not be allocated yet\nEnter donor ID: ", int)]
                },

            ],
            2: [  # Event & Projects Operations
                {
                    "name": "View event donations summary",
                    "function": lambda event_id: self.db.print_result(self.db.get_event_donations_summary(event_id)),
                    "args": [("event_id", "Enter event ID: ", int)]
                },
                {
                    "name": "View all events donations summary",
                    "function": lambda: self.db.print_result(self.db.get_all_events_donations_summary()),
                    "args": []
                },
                {
                    "name": "View Projects",
                    "function": lambda value: self.db.print_result(self.db.get_all('project')),
                    "args": []
                },
                {
                    "name": "View Project Objectives",
                    "function": lambda id: self.db.print_result(self.db.get_all(
                        'objective', 'objective.project_id', (id,))),
                    "args": [("Enter project ID: ", int)]
                }
            ],
            3: [  # Database Management
                {
                    "name": "Get column names (donor)",
                    "function": lambda: self.db.print_result(self.db.get_column_names('donor')),
                    "args": []
                }
            ]
        }
        
        self.current_category = None

    def display_welcome(self):
        print("\n" + "=" * 50)
        print("WELCOME TO DATABASE MANAGEMENT SYSTEM".center(50))
        print("=" * 50)

    def display_main_menu(self):
        print("\nMain Menu:")
        print("-" * 50)
        for i, category in enumerate(self.main_menu, 1):
            print(f"{i}. {category}")
        print("-" * 50)
        print("q - Quit application")
        print("-" * 50)

    def display_category_menu(self, category_idx):
        category_name = self.main_menu[category_idx]
        functions = self.category_functions[category_idx]
        
        print(f"\n{category_name} Menu:")
        print("-" * 50)
        for i, func in enumerate(functions, 1):
            print(f"{i}. {func['name']}")
        print("-" * 50)
        print("b - Back to main menu")
        print("q - Quit application")
        print("-" * 50)

    def get_user_input(self, prompt, data_type):
        while True:
            try:
                user_input = input(prompt)
                # Handle navigation commands
                if user_input.lower() in ['q', 'b', 'r']:
                    return user_input.lower()
                
                # Special case for optional input (like empty string for get_all_donors)
                if data_type == str and user_input == "":
                    return ""

                return data_type(user_input)
            except ValueError:
                print(f"Invalid input. Please enter a valid {data_type.__name__}.")

    def execute_function(self, category_idx, func_idx):
        if category_idx not in self.category_functions or func_idx < 0 or func_idx >= len(self.category_functions[category_idx]):
            print("Invalid option selected.")
            return
        
        func_info = self.category_functions[category_idx][func_idx]
        args = []
        
        for prompt, data_type in func_info["args"]:
            arg_value = self.get_user_input(prompt, data_type)
            if arg_value in ['q', 'b']:
                return arg_value
            args.append(arg_value)
        
        try:
            print("\nExecuting:", func_info["name"])
            print("-" * 50)
            func_info["function"](*args)
            print("-" * 50)
            input("\nPress Enter to continue...")
            return None
        except Exception as e:
            print(f"Error executing function: {e}")
            input("\nPress Enter to continue...")
            return None

    def handle_category_menu(self, category_idx):
        while True:
            self.display_category_menu(category_idx)
            choice = self.get_user_input("Enter your choice: ", str)
            
            if choice == 'q':
                self.running = False
                return
            elif choice == 'b':
                return
            
            try:
                func_idx = int(choice) - 1
                result = self.execute_function(category_idx, func_idx)
                if result == 'q':
                    self.running = False
                    return
                elif result == 'b':
                    return
            except ValueError:
                print("Invalid input. Please enter a number, 'b' to go back, or 'q' to quit.")

    def run(self):
        self.display_welcome()
        
        while self.running:
            self.display_main_menu()
            choice = self.get_user_input("Enter your choice: ", str)
            
            if choice == 'q':
                break
            
            try:
                category_idx = int(choice) - 1
                if 0 <= category_idx < len(self.main_menu):
                    self.handle_category_menu(category_idx)
                else:
                    print("Invalid category. Please select a number between 1 and", len(self.main_menu))
            except ValueError:
                print("Invalid input. Please enter a number or 'q' to quit.")
                print("Invalid input. Please enter a number or 'q' to quit.")


def main(db):
    app = DatabaseTerminalApp(db)
    app.run()
    print("\nThank you for using the Database Management System.")



