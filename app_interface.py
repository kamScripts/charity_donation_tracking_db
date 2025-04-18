
from db_handler import Db_handler
from populate_db import source
### add and check if args inside self.functions are correct

class DatabaseTerminalApp:
    def __init__(self, db: Db_handler):
        self.db = db
        self.running = True
        self.d_source = source
        self.table_names = ', '.join([' '.join(col) for col in self.db.get_table_names()])
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
                    "args": [("Enter donor name:", str)]
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
                    "args": [("Enter event ID: ", int)]
                },
                {
                    "name": "View all events donations summary",
                    "function": lambda: self.db.print_result(self.db.get_all_events_donations_summary()),
                    "args": []
                },
                {
                    "name": "View Projects",
                    "function": lambda: self.db.print_result(self.db.get_all('project')),
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
                    "name": "View table",
                    "function": lambda table: self.db.print_result(self.db.read_query(f'SELECT * FROM {table};')),
                    "args": [(f'Enter table name\n({self.table_names}):', str)]
                },
                {
                    "name": "Search by ID",
                    "function": lambda table, id: self.db.print_result(self.db.get_by_id(table, id)),
                    "args": [(f'Enter table name\n({self.table_names}):', str),
                             ('Enter ID:', int)]
                },
                {
                    "name": "insert new record",
                    "function": lambda table: self.handle_insert(table),
                    "args": [('Enter table name:', str),]
                },
                {
                    "name": "Delete record",
                    "function": lambda table, id: self.handle_delete(table, id),
                    "args": [('Enter table name:', str),
                             ('Enter id:', int)]
                },
                {
                    "name": "Update record",
                    "function": lambda table, id: self.handle_update(table, id),
                    "args": [
                                ("Enter table name: ", str),
                                ("Enter ID: ", int)
                            ]
                },
                
            ]
            
        }
    def handle_insert(self, table):
        try:
            # Get column names for the table
            column_names = self.db.get_column_names(table)[1:]

            if not column_names:
                print(f"No columns found for table '{table}' or table does not exist.")
                return

            print(f"\nTable '{table}' has the following columns:")
            print(", ".join(column_names))
            print("\nEnter values for each column (leave empty to omit):")

            # Collect columns and values
            columns = []
            values = []

            for column in column_names:
                value = input(f"{column}: ")
                if value != "":  # Only include non-empty values
                    columns.append(column)
                    # Try to convert numeric values
                    try:
                        # Try to convert to int or float if appropriate
                        if value.isdigit():
                            value = int(value)
                        #remove the first decimal point from the string and checks if the resulting string contains only digits.
                        #
                        elif value.replace('.', '', 1).isdigit() and value.count('.') <= 1:
                            value = float(value)
                    except ValueError:
                        pass   # Keep as string if conversion fails
                    values.append(value)

            if not columns:
                print("No values provided. Insert cancelled.")
                return

            # Insert the row
            self.db.insert_row(table, columns, values)
            

        except Exception as e:
            print(f"Error during insert operation: {e}")

    def handle_delete(self, table, id):
        prompt = "Confirm to delete a record (y / n): "
        try:
            row_to_delete = self.db.get_by_id(table, id)
            if table == 'donor' or table == 'event':
                print(f'Deleting {table} will delete all related donations')
                print('Row to delete: ', row_to_delete)
                dec = input(prompt)
                if dec.lower() == 'y':
                    match(table):
                        case 'donor':
                            self.db.delete_donor(id)
                        case 'event':
                            self.db.delete_event(id)
                    return
            else:
                print('Row to delete: ', row_to_delete)
                dec = input(prompt)
                if dec.lower() == 'y':
                    self.db.delete_record(table, id)
                return
        except Exception as e:
            print(f"Error during delete operation: {e}")

    def handle_update(self, table, id):
        """Handle the update of a record with dynamic columns."""
        try:
            # Get the record to be updated
            record = self.db.get_by_id(table, id)
            
            # Check if the record exists by checking if the DataFrame is empty
            if record is None or record.empty:
                print(f"No record found with ID {id} in table '{table}'.")
                return
                
            print(f"\nCurrent record: {record}")
            
            # Get column names for the table
            column_names = self.db.get_column_names(table)
            
            if not column_names:
                print(f"No columns found for table '{table}' or table does not exist.")
                return
            
            print(f"\nTable '{table}' has the following columns:")
            print(", ".join(column_names))
            print("\nEnter new values for each column (leave empty to keep current value):")
            
            # Collect columns and values to update
            columns = []
            values = []
            
            for column in column_names:
                if column.lower() == f'{table}_id':  # Skip ID column, it shouldn't be updated
                    continue
                    
                value = input(f"{column}: ")
                if value != "":  # Only include columns with new values
                    columns.append(column)
                    # Try to convert numeric values
                    try:
                        if value.isdigit():
                            value = int(value)
                        elif value.replace('.', '', 1).isdigit() and value.count('.') <= 1:
                            value = float(value)
                    except ValueError:
                        pass  # Keep as string if conversion fails
                    values.append(value)
            
            if not columns:
                print("No values provided. Update cancelled.")
                return
            
            # Convert values list to tuple as required by the function
            values_tuple = tuple(values)
            
            # Update the record
            self.db.update_records(table, id, columns, values_tuple)
            print(f"\nSuccessfully updated record with ID {id} in '{table}'.")
            
        except Exception as e:
            print(f"Error during update operation: {e}")


    def display_welcome(self):
        print("\n" + "=" * 50)
        print("WELCOME TO CHARITY DONATION TRACKING SYSTEM 1.0".center(50))
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
                if user_input.lower() in ['q', 'b']:
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
            return
        except Exception as e:
            print(f"Error executing function: {e}")
            input("\nPress Enter to continue...")
            return

    def handle_category_menu(self, category_idx):
        while True:
            self.display_category_menu(category_idx)
            choice = self.get_user_input("Enter your choice: ", str)
            
            if choice == 'q':
                self.running = False
                self.db.connection.close()
                return
            if choice == 'b':
                return
            
            try:
                func_idx = int(choice) - 1
                result = self.execute_function(category_idx, func_idx)
                if result == 'q':
                    self.running = False
                    self.db.connection.close()
                    return
                if result == 'b':
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
                    print(
                        "Invalid category. Please select a number between 1 and",
                        len(self.main_menu))
            except ValueError:
                print("Invalid input. Please enter a number or 'q' to quit.")
                print("Invalid input. Please enter a number or 'q' to quit.")


def main(db):
    app = DatabaseTerminalApp(db)
    app.run()
    print("\nThank you for using the Database Management System.")

