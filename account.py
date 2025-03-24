import mysql.connector 
from DB import DataBaseConnection

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
                    self._create_account()
                self._balance += amount
                self._record_transaction('Deposit', amount)
                print(f"Deposited {amount}. New balance: {self._balance}")
            else:
                print("Amount must be positive.")
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    def withdraw(self, amount):
        try:
            amount = float(amount)
            if amount > 0 and amount < self._balance:
                if not self._account_exists():
                    self._create_account()
                self._balance -= amount
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

class SavingsAccount(Account):
    def __init__(self, account_id, balance, interest_rate, min_balance):
        super().__init__(account_id, balance, 'savings')
        self._interest_rate = interest_rate
        self._min_balance = min_balance

    def withdraw(self, amount):
        try:
            amount = float(amount)
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
        self._overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        try:
            amount = float(amount)
            if self._balance - amount >= -self._overdraft_limit:
                self._balance -= amount
                self._record_transaction('Withdrawal', amount)
                print(f"Withdrew {amount}. New balance: {self._balance}")
            else:
                print("Withdrawal denied: Overdraft limit exceeded.")
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

def account_menu(account):
    while True:
        print("\nChoose an action:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Apply Interest ")
        print("5. View Transactions")
        print("6. Exit")

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
            account.list_transactions(account.cursor, account._account_id)  # Display transactions for the current account
        elif choice == '6':
            break
        else:
            print("Invalid choice or action not available for this account type.")

def get_account(cursor, account_id):
    try:
        cursor.execute("SELECT account_id, balance, account_type FROM Accounts WHERE account_id = %s", (account_id,))
        account = cursor.fetchone()
        if account:
            account_id, balance, account_type = account
            if account_type == 'savings':
                return SavingsAccount(account_id, balance, 0.05, 1000)  # Replace with actual interest_rate and min_balance
            elif account_type == 'current':
                return CurrentAccount(account_id, balance, 5000)  # Replace with actual overdraft_limit
        print(f"Account {account_id} not found.")
        return None
    except mysql.connector.Error as e:
        print(f"Error fetching account: {e}")
        return None

def account_choice():
    db_connection = DataBaseConnection()
    cursor = db_connection.cursor
    while True:
        print("\nChoose an action:")
        print("1. Create Account")
        print("2. Select Existing Account")
        print("3. Delete Account")
        print("4. View All Accounts")
        print("5. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            account_type = input("Enter account type (Savings/Current): ").lower()
            acc_id = input("Enter account ID: ")
            balance = float(input("Enter initial balance: "))
            if account_type == 'savings':
                interest_rate = float(input("Enter interest rate (e.g., 0.05 for 5%): "))
                min_balance = float(input("Enter minimum balance: "))
                savings = SavingsAccount(acc_id, balance, interest_rate, min_balance)
                account_menu(savings)
            elif account_type == 'current':
                overdraft_limit = float(input("Enter overdraft limit: "))
                current = CurrentAccount(acc_id, balance, overdraft_limit)
                account_menu(current)
            else:
                print("Invalid account type.")
        elif choice == '2':
            list_accounts(cursor)  # List all accounts
            account_id = input("Enter the account ID to select: ")
            account = get_account(cursor, account_id)
            if account:
                account_menu(account)
        elif choice == '3':
            print("Feature under development: Delete account.")
        elif choice == '4':
            list_accounts(cursor)  # Display all accounts
        elif choice == '5':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    account_choice()

if __name__ == "__main__":
    main()
