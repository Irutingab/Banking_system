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
            print(f"Error updating last active date: {e}")
            self.conn.rollback()

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
                return False

            amount = int(amount)
            if amount <= 0:
                print("Withdrawal amount must be positive.")
                return False

            interest = amount * 0.05
            total_withdrawal = amount + interest
            print(f"Trying to withdraw {amount} with an interest of {interest}. Total withdrawal: {total_withdrawal}")

            if self._balance - total_withdrawal >= self._min_balance:
                self._balance -= total_withdrawal
                self._update_balance()
                if self._record_transaction('Withdrawal', amount):
                    self._update_last_active()  # Update last_active after successful transaction
                    self._update_balance()  # Update balance after adding interest
                    print(f"Withdrew {amount}. Interest: {interest}. New balance: {self._balance}")
                    return True
                else:
                    # Rollback balance update if transaction recording fails
                    self._balance += total_withdrawal
                    self._update_balance()
                    return False
            else:
                print("Withdrawal denied: Insufficient funds to cover withdrawal and fee.")
                return False

        except ValueError:
            print("Amount must be a valid number.")
            return False
        except Exception as e:
            print(f"An error occurred during withdrawal: {e}")
            return False

    def deposit(self, amount):
        try:
            amount = int(amount)
            if amount <= 0:
                print("Deposit amount must be positive.")
                return False

            self._balance += amount
            if self._update_balance():
                if self._record_transaction('Deposit', amount):
                    self._update_last_active()  # Update last_active after successful transaction
                    print(f"Deposited {amount}. New balance: {self._balance}")
                    return True
                else:
                    # Rollback balance update if transaction recording fails
                    self._balance -= amount
                    self._update_balance()
                    return False
            else:
                # Rollback balance update if balance update fails
                self._balance -= amount
                return False

        except ValueError:
            print("Please enter a valid number.")
            return False
        except Exception as e:
            print(f"An error occurred during deposit transaction: {e}")
            return False

    def _record_transaction(self, transaction_type, amount):
        """Record a transaction in the database."""
        try:
            transaction_date = datetime.now()
            # Adjust the query to match the actual schema of the Transactions table
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

