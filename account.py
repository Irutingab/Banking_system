import mysql.connector 
from DB import DataBaseConnection
from decimal import Decimal  # Add this import

def list_accounts(cursor):
    try:
        cursor.execute("SELECT account_id, balance, account_type FROM Accounts")
        accounts = cursor.fetchall()
        if accounts:
            print("Existing Accounts:")
            for account in accounts:
                print(f"Account ID: {account[0]}, Balance: {account[1]}, Type: {account[2]}")
        else:
            print("No accounts found.")
    except mysql.connector.Error as e:
        print(f"Error fetching accounts: {e}")

def list_transactions(cursor, account_id):
    try:
        cursor.execute("SELECT transaction_id, transaction_type, amount, transaction_date FROM Transactions WHERE account_id = %s", (account_id,))
        transactions = cursor.fetchall()
        if transactions:
            print(f"Transactions for Account ID {account_id}:")
            for transaction in transactions:
                print(f"Transaction ID: {transaction[0]}, Type: {transaction[1]}, Amount: {transaction[2]}, Date: {transaction[3]}")
        else:
            print("No transactions found for this account.")
    except mysql.connector.Error as e:
        print(f"Error fetching transactions: {e}")

def list_customers(cursor):
    try:
        cursor.execute("SELECT customer_id, name, email, phone_number FROM Customers")
        customers = cursor.fetchall()
        if customers:
            print("Existing Customers:")
            for customer in customers:
                print(f"Customer ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}, Phone: {customer[3]}")
        else:
            print("No customers found.")
    except mysql.connector.Error as e:
        print(f"Error fetching customers: {e}")

def get_customer(cursor, customer_id):
    try:
        print(f"Fetching customer with ID: {customer_id}")  # Debug statement
        cursor.execute("SELECT customer_id, name, email, phone_number FROM Customers WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        if customer:
            print(f"Customer found: {customer}")  # Debug statement
            return customer
        print(f"Customer {customer_id} not found.")
        return None
    except mysql.connector.Error as e:
        print(f"Error fetching customer: {e}")
        return None

def add_customer(cursor, conn):
    try:
        name = input("Enter customer name: ")
        email = input("Enter customer email: ")
        phone_number = input("Enter customer phone number: ")
        cursor.execute(
            "INSERT INTO Customers (name, email, phone_number) VALUES (%s, %s, %s)",
            (name, email, phone_number)
        )
        conn.commit()
        print("Customer added successfully.")
    except mysql.connector.Error as e:
        print(f"Error adding customer: {e}")

def update_customer(cursor, conn, customer_id):
    try:
        name = input("Enter new customer name: ")
        email = input("Enter new customer email: ")
        phone_number = input("Enter new customer phone number: ")
        cursor.execute(
            "UPDATE Customers SET name = %s, email = %s, phone_number = %s WHERE customer_id = %s",
            (name, email, phone_number, customer_id)
        )
        conn.commit()
        print("Customer updated successfully.")
    except mysql.connector.Error as e:
        print(f"Error updating customer: {e}")

def customer_menu(cursor, conn):
    while True:
        print("\nChoose an action:")
        print("1. View Customer Details")
        print("2. Update Customer Details")
        print("3. Add New Customer")
        print("4. List All Customers")  # Add this line
        print("5. Exit")  # Update this line

        choice = input("Enter your choice: ")
        if choice == '1':
            customer_id = input("Enter customer ID: ")
            customer = get_customer(cursor, customer_id)
            if customer:
                print(f"Customer ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}, Phone: {customer[3]}")
        elif choice == '2':
            customer_id = input("Enter customer ID: ")
            customer = get_customer(cursor, customer_id)
            if customer:
                update_customer(cursor, conn, customer_id)
        elif choice == '3':
            add_customer(cursor, conn)
        elif choice == '4':  # Add this block
            list_customers(cursor)
        elif choice == '5':  # Update this line
            break
        else:
            print("Invalid choice. Please try again.")

class Account:
    def __init__(self, account_id, balance, account_type):
        self._account_id = account_id
        self._balance = balance
        self._account_type = account_type
        self.db_connection = DataBaseConnection()
        self.conn = self.db_connection.conn
        self.cursor = self.db_connection.cursor

    def _create_account(self):
        try:
            self.cursor.execute(
                "INSERT INTO Accounts (account_id, balance, account_type) VALUES (%s, %s, %s)",
                (self._account_id, self._balance, self._account_type)
            )
            self.conn.commit()
            print(f"Account {self._account_id} created in the database.")
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

    def deposit(self, amount):
        try:
            amount = float(amount)
            if amount > 0:
                if not self._account_exists():
                    print(f"Account {self._account_id} does not exist.")
                    return
                self._balance += amount
                self._update_balance()
                self._record_transaction('Deposit', amount)
                print(f"Deposited {amount}. New balance: {self._balance}")
            else:
                print("Amount must be positive.")
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    def withdraw(self, amount):
        try:
            amount = float(amount)
            if amount > 0 and amount <= self._balance:
                if not self._account_exists():
                    print(f"Account {self._account_id} does not exist.")
                    return
                self._balance -= amount
                self._update_balance()
                self._record_transaction('Withdrawal', amount)
                print(f"Withdrew {amount}. New balance: {self._balance}")
            else:
                print("Invalid amount or insufficient funds.")
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    def display_balance(self):
        print(f"Account {self._account_id} Balance: {self._balance}")

    def _account_exists(self):
        try:
            self.cursor.execute("SELECT 1 FROM Accounts WHERE account_id = %s", (self._account_id,))
            return self.cursor.fetchone() is not None
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return False

    def _record_transaction(self, transaction_type, amount):
        if not self._account_exists():
            print(f"Account {self._account_id} does not exist in the database.")
            return
        try:
            self.cursor.execute(
                "INSERT INTO Transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
                (self._account_id, transaction_type, amount)
            )
            self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

    def _update_balance(self):
        try:
            self.cursor.execute(
                "UPDATE Accounts SET balance = %s WHERE account_id = %s",
                (self._balance, self._account_id)
            )
            self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

class SavingsAccount(Account):
    def __init__(self, account_id, balance, interest_rate, min_balance):
        super().__init__(account_id, balance, 'savings')
        self._interest_rate = interest_rate
        self._min_balance = min_balance

    def _create_account(self):
        try:
            self.cursor.execute(
                "INSERT INTO Accounts (account_id, balance, account_type, interest_rate, min_balance) VALUES (%s, %s, %s, %s, %s)",
                (self._account_id, self._balance, self._account_type, self._interest_rate, self._min_balance)
            )
            self.conn.commit()
            print(f"Savings Account {self._account_id} created in the database.")
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

    def withdraw(self, amount):
        try:
            amount = Decimal(amount)  # Convert amount to Decimal
            if self._balance - amount >= self._min_balance:
                self._balance -= amount
                self._record_transaction('Withdrawal', amount)
                print(f"Withdrew {amount}. New balance: {self._balance}")
            else:
                print("Withdrawal denied: Minimum balance requirement not met.")
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    def apply_interest(self):
        interest = self._balance * self._interest_rate
        self._balance += interest
        self._record_transaction('Interest', interest)
        print(f"Interest applied. New balance: {self._balance}")

class CurrentAccount(Account):
    def __init__(self, account_id, balance, overdraft_limit):
        super().__init__(account_id, balance, 'current')
        self._overdraft_limit = overdraft_limit if overdraft_limit is not None else Decimal('0.00')  # Set default value

    def _create_account(self):
        try:
            self.cursor.execute(
                "INSERT INTO Accounts (account_id, balance, account_type, overdraft_limit) VALUES (%s, %s, %s, %s)",
                (self._account_id, self._balance, self._account_type, self._overdraft_limit)
            )
            self.conn.commit()
            print(f"Current Account {self._account_id} created in the database.")
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

    def withdraw(self, amount):
        try:
            amount = Decimal(amount)  # Convert amount to Decimal
            if self._balance - amount >= -self._overdraft_limit:
                self._balance -= amount
                self._record_transaction('Withdrawal', amount)
                print(f"Withdrew {amount}. New balance: {self._balance}")
            else:
                print("Withdrawal denied: Overdraft limit exceeded.")
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

def update_account(cursor, conn, account_id):
    try:
        balance = float(input("Enter new balance: "))
        account_type = input("Enter new account type (savings/current): ").lower()
        cursor.execute(
            "UPDATE Accounts SET balance = %s, account_type = %s WHERE account_id = %s",
            (balance, account_type, account_id)
        )
        conn.commit()
        print("Account updated successfully.")
    except mysql.connector.Error as e:
        print(f"Error updating account: {e}")
    except ValueError:
        print("Invalid input. Please enter valid numbers.")

def account_menu(account):
    while True:
        print("\nChoose an action:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Apply Interest")
        print("5. View Transactions")
        print("6. Update Account Details")  # Add this line
        print("7. Exit")  # Update this line

        choice = input("Enter your choice: ")
        if choice == '1':
            amount = input("Enter deposit amount: ")
            account.deposit(amount)
        elif choice == '2':
            amount = input("Enter withdrawal amount: ")
            account.withdraw(amount)
        elif choice == '3':
            account.display_balance()
        elif choice == '4' and isinstance(account, SavingsAccount):
            account.apply_interest()
        elif choice == '5':
            list_transactions(account.cursor, account._account_id)
        elif choice == '6':  # Add this block
            update_account(account.cursor, account.conn, account._account_id)
        elif choice == '7':  # Update this line
            break
        else:
            print("Invalid choice or action not available for this account type.")

def get_account(cursor, account_id):
    try:
        print(f"Fetching account with ID: {account_id}")  # Debug statement
        cursor.execute("SELECT account_id, balance, account_type, interest_rate, min_balance, overdraft_limit FROM Accounts WHERE account_id = %s", (account_id,))
        account = cursor.fetchone()
        if account:
            print(f"Account found: {account}")  # Debug statement
            account_id, balance, account_type, interest_rate, min_balance, overdraft_limit = account
            if account_type.lower() == 'savings':
                return SavingsAccount(account_id, balance, interest_rate, min_balance)
            elif account_type.lower() == 'current':
                return CurrentAccount(account_id, balance, overdraft_limit)
        print(f"Account {account_id} not found.")
        return None
    except mysql.connector.Error as e:
        print(f"Error fetching account: {e}")
        return None

def operate_existing_account(cursor):
    account_id = input("Enter account ID: ")
    account = get_account(cursor, account_id)
    if account:
        account_menu(account)
    else:
        print(f"Account {account_id} not found.")

def delete_account(cursor, conn, account_id):
    try:
        cursor.execute("DELETE FROM Accounts WHERE account_id = %s", (account_id,))
        conn.commit()
        print(f"Account {account_id} deleted successfully.")
    except mysql.connector.Error as e:
        print(f"Error deleting account: {e}")

def account_choice():
    db_connection = DataBaseConnection()
    cursor = db_connection.cursor
    conn = db_connection.conn
    while True:
        print("\nChoose an action:")
        print("1. Create Account")
        print("2. Manage Customers")
        print("3. Delete Account")
        print("4. View All Accounts")
        print("5. Operate Existing Account")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            account_type = input("Enter account type (Savings/Current): ").lower()
            acc_id = input("Enter account ID: ")
            balance = float(input("Enter initial balance: "))
            if account_type == 'savings':
                interest_rate = float(input("Enter interest rate (e.g., 0.05 for 5%): "))
                min_balance = float(input("Enter minimum balance: "))
                savings = SavingsAccount(acc_id, balance, interest_rate, min_balance)
                savings._create_account()
                account_menu(savings)
            elif account_type == 'current':
                overdraft_limit = float(input("Enter overdraft limit: "))
                current = CurrentAccount(acc_id, balance, overdraft_limit)
                current._create_account()
                account_menu(current)
            else:
                print("Invalid account type.")
        elif choice == '2':
            customer_menu(cursor, conn)
        elif choice == '3':
            account_id = input("Enter account ID to delete: ")
            delete_account(cursor, conn, account_id)  # Call the new function
        elif choice == '4':
            list_accounts(cursor)
        elif choice == '5':
            operate_existing_account(cursor)
        elif choice == '6':
            print("*** Exiting ***")
            break
        else:
            print("Invalid choice")

def main():
    account_choice()

if __name__ == "__main__":
    main()
