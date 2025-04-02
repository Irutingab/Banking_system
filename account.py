import mysql.connector 
from DB import DataBaseConnection

def get_customer(cursor, customer_id):
    try:
        print(f"Fetching customer with ID: {customer_id}")  
        cursor.execute("SELECT customer_id, name, email, phone_number FROM Customers WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        if customer:
            print(f"Customer found: {customer}")  
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
        print("1. Add New Customer")
        print("2. Update Customer Details")
        print("3. View Customer Details")  
        print("4. Exit")  

        choice = input("Enter your choice: ")
        if choice == '3':
            customer_id = input("Enter customer ID: ")
            customer = get_customer(cursor, customer_id)
            if customer:
                print(f"Customer ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}, Phone: {customer[3]}")
        elif choice == '2':
            customer_id = input("Enter customer ID: ")
            customer = get_customer(cursor, customer_id)
            if customer:
                update_customer(cursor, conn, customer_id)
        elif choice == '1':
            add_customer(cursor, conn)
        elif choice == '4':  
            break
        else:
            print("Invalid choice. Please try again.")

class Account:
    def __init__(self, account_id, balance, account_type, customer_id):
        self._account_id = account_id
        self._balance = balance
        self._account_type = account_type
        self._customer_id = customer_id  
        self.db_connection = DataBaseConnection()
        self.conn = self.db_connection.conn
        self.cursor = self.db_connection.cursor

    def _create_account(self):
        try:
            self.cursor.execute(
                "INSERT INTO Accounts (account_id, balance, account_type, customer_id) VALUES (%s, %s, %s, %s)",
                (self._account_id, self._balance, self._account_type, self._customer_id) 
            )
            self.conn.commit()
            print(f"Account {self._account_id} created in the database.")
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

    def deposit(self, amount):
        try:
            amount = int(amount)  
            if amount > 0:
                if not self._account_exists():
                    print(f"Account {self._account_id} does not exist.")
                    return
                self._balance += amount
                self._update_balance()  # Update the database with the new balance
                self._record_transaction('Deposit', amount)  # save the transaction
                print(f"Deposited {amount}. New balance: {self._balance}")
            else:
                print("Amount must be positive.")
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred during deposit: {e}")

    def withdraw(self, amount):
        try:
            amount = int(amount)  # Convert amount to integer
            if amount > 0:
                if not self._account_exists():
                    print(f"Account {self._account_id} does not exist.")
                    return
                if self._balance - amount >= 0:  # Ensure sufficient funds
                    self._balance -= amount
                    self._update_balance()  # Update the balance in the same account
                    self._record_transaction('Withdrawal', amount)  # Record the transaction
                    print(f"Withdrew {amount}. New balance: {self._balance}")
                else:
                    print("Insufficient balance.")
            else:
                print("Amount must be positive.")
        except ValueError:
            print("Please enter a valid amount.")

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
            # Update the balance in the existing account
            self.cursor.execute(
                "UPDATE Accounts SET balance = %s WHERE account_id = %s",
                (self._balance, self._account_id)
            )
            self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

class SavingsAccount(Account):
    def __init__(self, account_id, balance, interest_rate, min_balance, customer_id):
        super().__init__(account_id, int(balance), 'savings', customer_id) 
        self._interest_rate = int(interest_rate)  # Store interest rate as an integer (e.g., 5 for 5%)
        self._min_balance = int(min_balance)  

    def _create_account(self):
        try:
            self.cursor.execute(
                "INSERT INTO Accounts (account_id, balance, account_type, interest_rate, min_balance, customer_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (self._account_id, self._balance, self._account_type, self._interest_rate, self._min_balance, self._customer_id) 
            )
            self.conn.commit()
            print(f"Savings Account {self._account_id} created in the database.")
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

    def withdraw(self, amount):
        try:
            amount = int(amount) 
            print(f"Attempting to withdraw {amount} from account {self._account_id}") 
            print(f"Current balance: {self._balance}, Minimum balance: {self._min_balance}")  
            if self._balance - amount >= self._min_balance:
                self._balance -= amount
                self._update_balance()  # Update the database with the new balance
                self._record_transaction('Withdrawal', amount)  # Record the transaction
                print(f"Withdrew {amount}. New balance: {self._balance}")
            else:
                print("Withdrawal denied: Minimum balance requirement not met.")
        except ValueError:
            print("Invalid amount")
        except Exception as e:
            print(f"An error occurred during withdrawal: {e}")

    def apply_interest(self):
        try:
            interest = (self._balance * self._interest_rate) // 100  # Calculate interest as an integer
            self._balance += interest
            self._update_balance()  # Update the database with the new balance
            self._record_transaction('Interest', interest)  # Record the transaction
            print(f"Interest applied. New balance: {self._balance}")
        except Exception as e:
            print(f"An error occurred while applying interest: {e}")

class CurrentAccount(Account):
    def __init__(self, account_id, balance, overdraft_limit, customer_id):
        super().__init__(account_id, int(balance), 'current', customer_id)  
        if overdraft_limit is None or int(overdraft_limit) == 0:
            raise ValueError("Overdraft limit cannot be null or zero for a Current Account.")
        self._overdraft_limit = int(overdraft_limit)

    def _create_account(self):
        try:
            self.cursor.execute(
                "INSERT INTO Accounts (account_id, balance, account_type, overdraft_limit, customer_id) VALUES (%s, %s, %s, %s, %s)",
                (self._account_id, self._balance, self._account_type, self._overdraft_limit, self._customer_id)
            )
            self.conn.commit()
            print(f"Current Account {self._account_id} created in the database.")
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

    def withdraw(self, amount):
        try:
            amount = int(amount) 
            print(f"Attempting to withdraw {amount} from account {self._account_id}")  
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

def update_account(cursor, conn, account_id):
    try:
        balance = int(input("Enter new balance: "))
        account_type = input("Enter new account type (savings/current): ").lower()
        if account_type == 'current':
            overdraft_limit = int(input("Enter new overdraft limit: "))
            cursor.execute(
                "UPDATE Accounts SET balance = %s, account_type = %s, overdraft_limit = %s WHERE account_id = %s",
                (balance, account_type, overdraft_limit, account_id)
            )
        else:
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
            update_account(account.cursor, account.conn, account._account_id)
        elif choice == '5':  
            break
        else:
            print("Invalid choice or action not available for this account type.")

def get_account(cursor, account_id):
    try:
        print(f"Fetching account with ID: {account_id}")  
        cursor.execute("SELECT account_id, balance, account_type, interest_rate, min_balance, overdraft_limit, customer_id FROM Accounts WHERE account_id = %s", (account_id,))
        account = cursor.fetchone()
        if account:
            print(f"Account found: {account}") 
            account_id, balance, account_type, interest_rate, min_balance, overdraft_limit, customer_id = account
            if account_type.lower() == 'savings':
                return SavingsAccount(account_id, balance, interest_rate, min_balance, customer_id)
            elif account_type.lower() == 'current':
                return CurrentAccount(account_id, balance, overdraft_limit, customer_id)
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
        # Delete the account and related transactions
        cursor.execute("DELETE FROM Accounts WHERE account_id = %s", (account_id,))
        conn.commit()
        print(f"Account {account_id} deleted successfully.")
    except mysql.connector.Error as e:
        print(f"Error deleting account: {e}")

def create_account(cursor, connection):
    account_type = input("Enter account type (Savings/Current): ").capitalize()
    customer_id = int(input("Enter customer ID: "))
    initial_balance = int(input("Enter initial balance: "))

    if account_type == "Savings":
        interest_rate = int(input("Enter interest rate (e.g., 5 for 5%): "))
        min_balance = int(input("Enter minimum balance: "))
        query = """
            INSERT INTO Accounts (account_type, balance, interest_rate, min_balance, customer_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (account_type, initial_balance, interest_rate, min_balance, customer_id)
    elif account_type == "Current":
        overdraft_limit = int(input("Enter overdraft limit: "))
        query = """
            INSERT INTO Accounts (account_type, balance, overdraft_limit, customer_id)
            VALUES (%s, %s, %s, %s)
        """
        values = (account_type, initial_balance, overdraft_limit, customer_id)
    else:
        print("Invalid account type.")
        return

    try:
        cursor.execute(query, values)
        connection.commit()
        print(f"{account_type} Account created successfully.")
    except Exception as e:
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
            account_id = input("Enter account ID to delete: ")
            delete_account(cursor, conn, account_id)  
        elif choice == '4':
            operate_existing_account(cursor)
        elif choice == '5':
            print("*** Exiting ***")
            break
        else:
            print("Invalid choice")


