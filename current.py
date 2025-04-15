from account import Account
import mysql.connector
from savings import SavingsAccount
from customer import customer_menu
from DB import DataBaseConnection
from datetime import datetime


class CurrentAccount(Account):
    def __init__(self, account_number, balance, overdraft_limit, customer_id):
        super().__init__(account_number, int(balance), 'current', customer_id)
        
        if overdraft_limit is None or int(overdraft_limit) == 0:
            raise ValueError("Overdraft limit cannot be null")
        self._overdraft_limit = int(overdraft_limit)
        self._fetch_account_status()

    def _fetch_account_status(self):
        try:
            self.cursor.execute(
                "SELECT account_status FROM Accounts WHERE account_number = %s",
                (self._account_number,)
            )
            status_result = self.cursor.fetchone()
            if status_result:
                self._account_status = status_result[0]
            else:
                self._account_status = 'status not defined'
        except mysql.connector.Error as e:
            print(f"Error fetching account status: {e}")

    def _create_account(self):
        try:
            self.cursor.execute(
                "INSERT INTO Accounts (account_number, balance, account_type, overdraft_limit, customer_id) VALUES (%s, %s, %s, %s, %s)",
                (self._account_number, self._balance, self._account_type, self._overdraft_limit, self._customer_id)
            )
            self.conn.commit()
            print(f"Current Account {self._account_number} created in the database.")
        except mysql.connector.Error as e:
            print(f"Database related error: {e}")

    def deposit(self, amount):
        try:
            self._fetch_account_status()

            if self._account_status == 'deleted':
                print("This account is deleted, deposits are not allowed.")
                return False

            amount = int(amount)
            if amount <= 0:
                print("Deposit amount must be greater than zero.")
                return False

            self._balance += amount
            self.cursor.execute(
                "UPDATE Accounts SET balance = %s WHERE account_number = %s",
                (self._balance, self._account_number)
            )
            self.conn.commit()
            self._record_transaction('Deposit', amount)
            print(f"Successfully deposited {amount}. New balance: {self._balance}")
            return True
        except ValueError:
            print("Please enter a valid number.")
            return False
        except mysql.connector.Error as e:
            print(f"An error occurred in the database, Please try again!: {e}")
            self.conn.rollback()
            return False

    def withdraw(self, amount):
        try:
            self._fetch_account_status()

            if self._account_status == 'inactive':
                print("This account is currently inactive. You can only make deposits.")
                return False
            elif self._account_status == 'deleted':
                print("This account is deleted, deposits are not allowed.")
                return False

            amount = int(amount)
            print(f"Current balance: {self._balance}, Overdraft limit: {self._overdraft_limit}")
            if self._balance - amount >= -self._overdraft_limit:
                self._balance -= amount
                self._update_balance()
                self._record_transaction('Withdrawal', amount)
                print(f"Withdrew {amount}. New balance: {self._balance}")
                return True
            else:
                print("Overdraft limit exceeded, Please try again!")
                return False
        except ValueError:
            print("Please enter a valid number.")
            return False
        except Exception as e:
            print(f"An error occurred during your withdrawal, Please try again: {e}")
            return False

    def _record_transaction(self, transaction_type, amount):
        try:
            transaction_date = datetime.now()
            self.cursor.execute(
                "INSERT INTO Transactions (account_number, transaction_type, amount, transaction_date) VALUES (%s, %s, %s, %s)",
                (self._account_number, transaction_type, amount, transaction_date)
            )
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error recording transaction: {e}")
            self.conn.rollback()
            return False

def update_account(cursor, conn, account_number):
    try:
        cursor.execute("SELECT account_type, overdraft_limit, interest_rate, min_balance FROM Accounts WHERE account_number = %s", (account_number,))
        Existing_info = cursor.fetchone()
        
        if not Existing_info:
            print("Account details not found in the database.")
            return

        account_type, current_overdraft, current_interest, current_min_balance = Existing_info
        print(" Leave input blank to keep the current value.\n")

        if account_type.lower() == 'current':
            overdraft_input = input(f"Enter new overdraft limit (current: {current_overdraft}): ")
            if overdraft_input.strip() != "":
                overdraft_limit = int(overdraft_input)
                cursor.execute(
                    "UPDATE Accounts SET overdraft_limit = %s WHERE account_number = %s",
                    (overdraft_limit, account_number)
                )
                conn.commit()
                print("Overdraft limit updated successfully.")
            else:
                print("Overdraft limit remained unchanged.")

        elif account_type.lower() == 'savings':
            interest_input = input(f"Enter new interest rate (current: {current_interest}%): ")
            min_balance_input = input(f"Enter new minimum balance (current: {current_min_balance}): ")
            if min_balance_input.strip() != "":
                min_balance = int(min_balance_input)
                cursor.execute(
                    "UPDATE Accounts SET min_balance = %s WHERE account_number = %s",
                    (min_balance, account_number)
                )
                conn.commit()
                print("Minimum balance updated successfully.")
            else:
                print("Minimum balance remained unchanged.")

            if interest_input.strip() != "":
                interest_rate = int(interest_input)
                cursor.execute(
                    "UPDATE Accounts SET interest_rate = %s WHERE account_number = %s",
                    (interest_rate, account_number)
                )
                conn.commit()
                print("Interest rate updated successfully.")
            else:
                print("Interest rate unchanged.")

        else:
            print(" Unknown account error.")

    except mysql.connector.Error as e:
        print(f" DB Error: {e}")
    except ValueError:
        print("Please enter a valid number from the provided list")

def account_menu(account):
    while True:
        print("\nChoose an action:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Update Account Details")  
        print("5. Exit") 

        choice = input("Enter your choice: ")
        if choice == '1':
            amount = input("Enter deposit amount: ")
            account.deposit(amount)
        elif choice == '2':
            amount = input("Enter withdrawal amount: ")
            account.withdraw(amount)
        elif choice == '3':
            account.display_balance()
        elif choice == '4':  
            update_account(account.cursor, account.conn, account._account_number)
        elif choice == '5':  
            break
        else:
            print("Invalid choice.")

def get_account(cursor, account_number):
    try:
        print(f"Retrieving account with number: {account_number}")  
        cursor.execute(
"SELECT account_number, balance, account_type, interest_rate, min_balance, overdraft_limit, customer_id "
            "FROM Accounts WHERE account_number = %s", 
(account_number,)
)
        account = cursor.fetchone()
        if account:

            print(f"(account_number: {account[0]}, balance: {account[1]}, account_type: {account[2]}, interest_rate: {account[3]}, min_balance: {account[4]}, overdraft_limit: {account[5]}, customer_id: {account[6]})")
            
            account_number, balance, account_type, interest_rate, min_balance, overdraft_limit, customer_id = account
            if account_type.lower() == 'savings':
                return SavingsAccount(account_number, balance, interest_rate, min_balance, customer_id)
            elif account_type.lower() == 'current':
                return CurrentAccount(account_number, balance, overdraft_limit, customer_id)

        print(f"Account {account_number} Does not exist.")
        return None
    except mysql.connector.Error as e:
        print(f"Account {account_number} not found in the database: {e}")
        return None

def operate_existing_account(cursor):
    account_number = input("Enter account number: ")
    account = get_account(cursor, account_number)
    if account:
        account_menu(account)
    else:
        print(f"Account {account_number} not found in the database.")

def create_account(cursor, connection):
    while True:
        account_type = input("Enter account type savings or current: ")
        if account_type not in ['savings', 'current']:
            print("Error: Accounts are written in lowercase")
            continue
        break
    
    while True:
        customer_id = int(input("Enter customer ID: "))
        cursor.execute("SELECT customer_id FROM Customers WHERE customer_id = %s", (customer_id,))
        if cursor.fetchone():
            break
        else:
            print("The provided customer ID does not exist")

    while True:
        account_number = input("Enter a unique 9-digit account number: ")
        if not account_number.isdigit() or len(account_number) != 9:
            print("Account number must be exactly 9 digits ")
            continue
        
        cursor.execute("SELECT account_number FROM Accounts WHERE account_number = %s", (account_number,))
        if cursor.fetchone():
            print(f"Account number {account_number} already exists. Please choose a different one.")
        else:
            break
            
    while True:
        initial_balance_input = input("Enter initial balance: ")
        if not initial_balance_input.strip():
            print("Initial balance cannot be null.")
            continue
        try:
            initial_balance = int(initial_balance_input)
            if initial_balance < 0:
                print("Initial balance must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid value for the initial balance.")

    if account_type == "savings":
        while True:
            interest_rate = int(input("Enter interest rate (example, 5 for 5%): "))
            if interest_rate >= 20:
                print("Interest rate must be less than 20")
                continue
            break
        min_balance = int(input("Enter minimum balance: "))
        query = """
            INSERT INTO Accounts (account_number, account_type, balance, interest_rate, min_balance, customer_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (account_number, account_type, initial_balance, interest_rate, min_balance, customer_id)
    elif account_type == "current":
        overdraft_limit = int(input("Enter overdraft limit: "))
        query = """
            INSERT INTO Accounts (account_number, account_type, balance, overdraft_limit, customer_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (account_number, account_type, initial_balance, overdraft_limit, customer_id)
    else:
        print("Inexisting account type.")
        return

    try:
        cursor.execute(query, values)
        connection.commit()
        print(f"Account {account_number} created successfully, and saved in the database.")
    except mysql.connector.Error as e:
        print(f"Database related error: {e}")

def check_account_status(cursor):
    account_number = input("Enter the account number to verify its status: ")
    try:
        cursor.execute(
            "SELECT account_status FROM Accounts WHERE account_number = %s",
            (account_number,)
        )
        result = cursor.fetchone()
        if result:
            account_status = result[0]
            print(f"Account {account_number} is currently {account_status}.")
        else:
            print(f"Account {account_number} does not exist.")
    except mysql.connector.Error as e:
        print(f"An error occurred while checking account status: {e}")

def account_choice():

    db_connection = DataBaseConnection()
    cursor = db_connection.get_cursor()
    conn = db_connection.get_connection()
    
    while True:
        print("\nChoose an action:")
        print("1. Manage Customers")
        print("2. Create Account")
        print("3. Operate Existing Account")
        print("4. Check Account Status") 
        print("5. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            customer_menu(cursor, conn) 
        elif choice == '2':
            create_account(cursor, conn) 
        elif choice == '3':
            operate_existing_account(cursor)
        elif choice == '4': 
            check_account_status(cursor)
        elif choice == '5':
            print("___ Exiting ___")
            break
        else:
            print("Invalid choice")


