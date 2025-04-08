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
            status_result = self.cursor.fetchone()
            if status_result:
                self._account_status = status_result[0]
            else:
                self._account_status = 'status not defined'  
        except mysql.connector.Error as e:
            print(f"Error fetching account status: {e}")

    def _update_last_active(self):
        try:
            current_date = datetime.now().date()
            self.cursor.execute(
                "UPDATE Accounts SET last_active = %s WHERE account_number = %s",
                (current_date, self._account_number)
            )
            self.conn.commit()
        except mysql.connector.Error as e:
            print(f"An Error occured while updating last active date: {e}")

    def _create_account(self):
        try:
            self.cursor.execute(
                "INSERT INTO Accounts (account_number, balance, account_type, interest_rate, min_balance, customer_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (self._account_number, self._balance, self._account_type, self._interest_rate, self._min_balance, self._customer_id) 
            )
            self.conn.commit()
            print(f"Savings Account {self._account_number} created in the database.")
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

    def withdraw(self, amount):
        try:
            self._fetch_account_status()  
            
            if self._account_status == 'disabled':
                print("This account is currently disabled. You can only make deposits.")
                return
                
            amount = int(amount) 
            interest = amount * 0.05  

            total_withdrawal = amount + interest 
            print(f"Trying to withdraw {amount} with an interest of {interest}. Total withdrawal: {total_withdrawal}")

            if self._balance - total_withdrawal >= self._min_balance:
                self._balance -= total_withdrawal 
                self._update_balance() 
                self._record_transaction('Withdrawal', amount)  
                self._update_last_active()  
                print(f"Withdrew {amount}. interest: {interest}. New balance: {self._balance}")
            else:
                print("Withdrawal denied: Insufficient funds to cover withdrawal and fee.")

        except ValueError:
            print("Minimum_balance must be a positive number.")
        except Exception as e:
            print(f"An error occurred during withdrawal: {e}")
            
    def deposit(self, amount):
        try:
            amount = int(amount)
            if amount <= 0:
                print("Deposit amount must be positive.")
                return False
                
            self._balance += amount
            self._update_balance()
            self._record_transaction('Deposit', amount)
            self._update_last_active()  
            print(f"Deposited {amount}")
            return True
        except ValueError:
            print("Please enter a valid number.")
            return False
        except Exception as e:
            print(f"An error occurred during deposit transaction: {e}")
            return False

