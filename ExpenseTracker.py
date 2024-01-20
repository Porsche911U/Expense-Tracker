import json
import datetime

USER_DATA_FILE = "user_data.json"

expenses = {}

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return super().default(obj)

def print_header(title):
    print("=" * 30)
    print(title.center(30))
    print("=" * 30)

def load_data():
    try:
        with open(USER_DATA_FILE, 'r') as file:
            data = file.read()
            if data:
                return json.loads(data)
            else:
                return {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=2, cls=DateEncoder)

def signup():
    print_header("Sign Up")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    users = load_data()

    if username not in users:
        users[username] = {'password': password, 'expenses': []}
        save_data(users)
        print("Account created successfully. You can now log in.")
    else:
        print("Username already exists. Please choose a different one.")

def login():
    print_header("Login")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    users = load_data()

    if username in users and users[username]['password'] == password:
        print("Login successful.")
        return username
    else:
        print("Invalid username or password. Please try again.")
        return None

def add_expense(username):
    print("Add Expense")

    amount = float(input("Enter the expense amount: "))
    description = input("Enter a brief description: ")
    date_str = input("Enter the expense date (YYYY-MM-DD): ")

    try:
        expense_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    expense = {
        'amount': amount,
        'description': description,
        'date': expense_date
    }

    users = load_data()
    users[username]['expenses'].append(expense)
    save_data(users)

    print("Expense added successfully!")

def view_expenses(username):
    print("View Expenses")

    users = load_data()
    if username in users and users[username]['expenses']:
        for index, expense in enumerate(users[username]['expenses'], start=1):
            print(f"{index}. Date: {expense['date']}, Amount: ${expense['amount']}, Description: {expense['description']}")
    else:
        print("No expenses found.")
        
def update_expense(username):
    print("Update Expense")

    users = load_data()
    if username in users and users[username]['expenses']:
        view_expenses(username)  
        try:
            expense_index = int(input("Enter the index of the expense to update: ")) - 1
            if 0 <= expense_index < len(users[username]['expenses']):
                amount = float(input("Enter the new expense amount: "))
                description = input("Enter the new description: ")
                date_str = input("Enter the new expense date (YYYY-MM-DD): ")
                new_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

                users[username]['expenses'][expense_index] = {
                    'amount': amount,
                    'description': description,
                    'date': new_date
                }
                save_data(users)
                print("Expense updated successfully!")
            else:
                print("Invalid expense index. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid index.")
    else:
        print("No expenses found.")

def delete_expense(username):
    print("Delete Expense")

    users = load_data()
    if username in users and users[username]['expenses']:
        view_expenses(username)  
        try:
            expense_index = int(input("Enter the index of the expense to delete: ")) - 1
            if 0 <= expense_index < len(users[username]['expenses']):
                del users[username]['expenses'][expense_index]
                save_data(users)
                print("Expense deleted successfully!")
            else:
                print("Invalid expense index. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid index.")
    else:
        print("No expenses found.")
        
    

def main():
    while True:
        print_header("Expense Tracker")
        print("1. Sign Up")
        print("2. Login")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            signup()
        elif choice == '2':
            username = login()
            if username:
                while True:
                    print_header("Expense Tracker")
                    print("1. Add Expense")
                    print("2. View Expenses")
                    print("3. update_expense")
                    print("4. delete_expense")
                    print("5. Logout")

                    user_choice = input("Enter your choice: ")

                    if user_choice == '1':
                        add_expense(username)
                    elif user_choice == '2':
                        view_expenses(username)
                    elif user_choice == '3':
                        update_expense(username)
                    elif user_choice == '4':
                        delete_expense(username)    
                    elif user_choice == '5':
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '3':
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

main()
