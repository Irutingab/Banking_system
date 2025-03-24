import mysql.connector 
from DB import DataBaseConnection

class Account:
    def __init__(self, account_number, balance):
        self._account_number = account_number  
        self._balance = balance  
        self.db_connection = DataBaseConnection()
        self.conn = self.db_connection.conn
        self.cursor = self.db_connection.cursor

    def deposit(self, amount):
        try:
            amount = float(amount)
            if amount > 0:
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
                self._balance -= amount
                self._record_transaction('Withdrawal', amount)
                print(f"Withdrew {amount}. New balance: {self._balance}")
            else:
                print("Invalid amount or insufficient funds.")
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    def display_balance(self):
        print(f"Account {self._account_number} Balance: {self._balance}")

    def _record_transaction(self, transaction_type, amount):
        try:
            self.cursor.execute(
                "INSERT INTO Transactions (account_number, transaction_type, amount) VALUES (%s, %s, %s)",
                (self._account_number, transaction_type, amount)
            )
            self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

class SavingsAccount(Account):
    def __init__(self, account_number, balance, interest_rate, min_balance):
        super().__init__(account_number, balance)
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
    def __init__(self, account_number, balance, overdraft_limit):
        super().__init__(account_number, balance)
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
        print("4. Apply Interest (Savings only)")
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
        elif choice == '4' and isinstance(account, SavingsAccount):
            account.apply_interest()
        elif choice == '5':
            break
        else:
            print("Invalid choice or action not available for this account type.")

def account_choice():
    while True:
        print("\nChoose an account type:")
        print("1. Savings Account")
        print("2. Current Account")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            acc_num = input("Enter account number: ")
            balance = float(input("Enter initial balance: "))
            interest_rate = float(input("Enter interest rate (e.g., 0.05 for 5%): "))
            min_balance = float(input("Enter minimum balance: "))
            savings = SavingsAccount(acc_num, balance, interest_rate, min_balance)
            account_menu(savings)
        elif choice == '2':
            acc_num = input("Enter account number: ")
            balance = float(input("Enter initial balance: "))
            overdraft_limit = float(input("Enter overdraft limit: "))
            current = CurrentAccount(acc_num, balance, overdraft_limit)
            account_menu(current)
        elif choice == '3':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    account_choice()

if __name__ == "__main__":
    main()

