from account import Account
import mysql.connector
from datetime import datetime

class SavingsAccount(Account):
    def __init__(self, account_number, balance, interest_rate, min_balance, customer_id):
        super().__init__(account_number, int(balance), 'savings', customer_id) 
        
        self._interest_rate = int(interest_rate)  
        self._min_balance = int(min_balance)
        self._fetch_account_status()  
        
    def _fetch_account_status(self):
        try:
            self.cursor.execute(
                "SELECT account_status FROM Accounts WHERE account_number = %s",
                (self._account_number,)
            )
            
            account_status_result = self.cursor.fetchone()
            if account_status_result:
                self._account_status = account_status_result[0]
            else:
                self._account_status = 'status not defined'  
        except mysql.connector.Error as e:
            print(f"Error fetching account status: {e}")

    def _create_account(self):
        try:
            self.cursor.execute(
                "INSERT INTO Accounts (account_number, balance, account_type, interest_rate, min_balance, customer_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (self._account_number, self._balance, self._account_type, self._interest_rate, self._min_balance, self._customer_id) 
            )
            self.conn.commit()
            print(f"Savings Account {self._account_number} created in the database.")
        except mysql.connector.Error as e:
            print(f"An error occured while connecting to the DB: {e}")

    def withdraw(self, amount):
        try:
            self._fetch_account_status()
            
            if self._account_status == 'inactive':
                print("This account is currently inactive. You can only make deposits.")
                return False
            elif self._account_status == 'deleted':
                print("This account cannot be used as it has been deleted.")
                return False

            amount = int(amount)
            if amount <= 0:
                print("Withdrawal amount must be positive.")
                return False
            #get interest rate  from the database
            self.cursor.execute(
                "SELECT interest_rate FROM Accounts WHERE account_number = %s",
                (self._account_number,)
            )
            interest_rate_result = self.cursor.fetchone()
            if not interest_rate_result:
                print("An error occurred while fetching interest rate for this account.")
                return False

            interest_rate = interest_rate_result[0] / 100 
            interest = amount * interest_rate
            total_withdrawal = amount + interest

            if self._balance - total_withdrawal > self._min_balance:
                self._balance -= total_withdrawal
                self._update_balance()
                if self._record_transaction('Withdrawal', amount):
                    print(f"Withdrew {amount}. Interest: {interest:.2f}. Your total withdrawal: {total_withdrawal}")
                    return True
            else:
                print("Withdrawal denied: Your funds can't cover withdrawal and minimum balance.")
                return False

        except Exception as e:
            print(f"An error occurred during withdrawal: {e}")
            return False
    def deposit(self, amount):
        try:
            self._fetch_account_status()
            if self._account_status == 'deleted':
                print("This account cannot be used as it has been deleted.")
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
            print(f"Error occurred while recording transaction: {e}")
            self.conn.rollback()
            return False

