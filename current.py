from account import Account
import mysql.connector
from savings import SavingsAccount
from customer import customer_menu
from DB import DataBaseConnection
class CurrentAccount(Account):
    def __init__(self, account_number, balance, overdraft_limit, customer_id):
        super().__init__(account_number, int(balance), 'current', customer_id)  
        if overdraft_limit is None or int(overdraft_limit) == 0:
            raise ValueError("Overdraft limit cannot be null or zero for a Current Account.")
        self._overdraft_limit = int(overdraft_limit)

    def _create_account(self):
        try:
            self.cursor.execute(
                "INSERT INTO Accounts (account_number, balance, account_type, overdraft_limit, customer_id) VALUES (%s, %s, %s, %s, %s)",
                (self._account_number, self._balance, self._account_type, self._overdraft_limit, self._customer_id)
            )
            self.conn.commit()
            print(f"Current Account {self._account_number} created in the database.")
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

    def withdraw(self, amount):
        try:
            amount = int(amount) 
            print(f"Attempting to withdraw {amount} from account {self._account_number}")  
            print(f"Current balance: {self._balance}, Overdraft limit: {self._overdraft_limit}")  
            if self._balance - amount >= -self._overdraft_limit:
                self._balance -= amount
                self._update_balance()  # Update the database with the new balance
                self._record_transaction('Withdrawal', amount)  # Record the transaction
                print(f"Withdrew {amount}. New balance: {self._balance}")
            else:
                print("Withdrawal denied: Overdraft limit exceeded.")
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred during withdrawal: {e}")

def update_account(cursor, conn, account_number):
    try:
        balance = int(input("Enter new balance: "))
        account_type = input("Enter new account type (savings/current): ").lower()
        if account_type == 'current':
            overdraft_limit = int(input("Enter new overdraft limit: "))
            cursor.execute(
                "UPDATE Accounts SET balance = %s, account_type = %s, overdraft_limit = %s WHERE account_number = %s",
                (balance, account_type, overdraft_limit, account_number)
            )
        else:
            cursor.execute(
                "UPDATE Accounts SET balance = %s, account_type = %s WHERE account_number = %s",
                (balance, account_type, account_number)
            )
        conn.commit()
        print("Account updated successfully.")
    except mysql.connector.Error as e:
        print(f"Error updating account: {e}")
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
    except Exception as e:
        print(f"An error occurred: {e}")    

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
            print("Invalid choice or action not available for this account type.")

def get_account(cursor, account_number):
    try:
        print(f"Fetching account with number: {account_number}")  
        cursor.execute("SELECT account_number, balance, account_type, interest_rate, min_balance, overdraft_limit, customer_id FROM Accounts WHERE account_number = %s", (account_number,))
        account = cursor.fetchone()
        if account:
            print(f"Account found: {account}") 
            account_number, balance, account_type, interest_rate, min_balance, overdraft_limit, customer_id = account
            if account_type.lower() == 'savings':
                return SavingsAccount(account_number, balance, interest_rate, min_balance, customer_id)
            elif account_type.lower() == 'current':
                return CurrentAccount(account_number, balance, overdraft_limit, customer_id)
        print(f"Account {account_number} not found.")
        return None
    except mysql.connector.Error as e:
        print(f"Error fetching account: {e}")
        return None

def operate_existing_account(cursor):
    account_number = input("Enter account number: ")
    account = get_account(cursor, account_number)
    if account:
        account_menu(account)
    else:
        print(f"Account {account_number} not found.")

def delete_account(cursor, conn, account_number):
    try:
        # Delete the account and related transactions
        cursor.execute("DELETE FROM Accounts WHERE account_number = %s", (account_number,))
        conn.commit()
        print(f"Account {account_number} deleted successfully.")
    except mysql.connector.Error as e:
        print(f"Error deleting account: {e}")

def create_account(cursor, connection):
    account_type = input("Enter account type (Savings/Current): ").capitalize()
    
    while True:
        customer_id = int(input("Enter customer ID: "))
        cursor.execute("SELECT 1 FROM Customers WHERE customer_id = %s", (customer_id,))
        if cursor.fetchone():
            break
        else:
            print(f"Customer ID {customer_id} does not exist. Please enter a valid customer ID.")

    account_number = input("Enter a unique 9-digit account number: ")
    initial_balance = int(input("Enter initial balance: "))

    if account_type == "Savings":
        interest_rate = int(input("Enter interest rate (e.g., 5 for 5%): "))
        min_balance = int(input("Enter minimum balance: "))
        query = """
            INSERT INTO Accounts (account_number, account_type, balance, interest_rate, min_balance, customer_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (account_number, account_type, initial_balance, interest_rate, min_balance, customer_id)
    elif account_type == "Current":
        overdraft_limit = int(input("Enter overdraft limit: "))
        query = """
            INSERT INTO Accounts (account_number, account_type, balance, overdraft_limit, customer_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (account_number, account_type, initial_balance, overdraft_limit, customer_id)
    else:
        print("Invalid account type.")
        return

    try:
        cursor.execute(query, values)
        connection.commit()
        print(f"{account_type} Account with number {account_number} created successfully.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")

def account_choice():
    db_connection = DataBaseConnection()
    cursor = db_connection.cursor
    conn = db_connection.conn
    while True:
        print("\nChoose an action:")
        print("1. Create Account")
        print("2. Manage Customers")
        print("3. Delete Account")
        print("4. Operate Existing Account")
        print("5. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            create_account(cursor, conn)  
        elif choice == '2':
            customer_menu(cursor, conn)
        elif choice == '3':
            account_number = input("Enter account number to delete: ")
            delete_account(cursor, conn, account_number)  
        elif choice == '4':
            operate_existing_account(cursor)
        elif choice == '5':
            print("*** Exiting ***")
            break
        else:
            print("Invalid choice")


