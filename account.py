import mysql.connector 
from DB import DataBaseConnection
from datetime import datetime

class Account:
    def __init__(self, account_number, balance, account_type, customer_id):
        self._account_number = account_number  
        self._balance = balance
        self._account_type = account_type
        self._customer_id = customer_id  
        self.db_connection = DataBaseConnection()
        self.conn = self.db_connection.get_connection()
        self.cursor = self.db_connection.get_cursor()

    def _create_account(self):
        try:
            self.cursor.execute( 
                "INSERT INTO Accounts (account_number, balance, account_type, customer_id) VALUES (%s, %s, %s, %s)",
                (self._account_number, self._balance, self._account_type, self._customer_id) 
            )
            self.conn.commit()
            print(f"Account {self._account_number} created and saved in the database.")
        except mysql.connector.Error as e:
            print(f"Error connecting to the database: {e}")
            
    def _record_transaction(self, transaction_type, amount, description=None):
        try:
            transaction_date = datetime.now()
            self.cursor.execute(
                "INSERT INTO Transactions (account_number, transaction_type, amount, transaction_date, description) VALUES (%s, %s, %s, %s, %s)",
                (self._account_number, transaction_type, amount, transaction_date, description)
            )
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print(f"An error occurred while recording transaction: {e}")
            self.conn.rollback()
            return False

    def deposit(self, amount):
        try:
            amount = int(amount)
            if amount > 0:
                if not self._account_exists():
                    print(f"Account {self._account_number} does not exist.")
                    return
                
                self._balance += amount
                self._update_balance()  
                self._record_transaction('Deposit', amount) 
                print(f"Deposited {amount} New balance: {self._balance}")
            else:
                print("Amount must be positive.")
        except ValueError:
            print("Please enter a valid number from the displayed list.")
        except Exception as e:
            print(f"An error occurred during your deposit, Kindly try again! {e}")

    def withdraw(self, amount):
        try:
            amount = int(amount)
            if amount > 0:
                if not self._account_exists():
                    print(f"Account {self._account_number} does not exist.")
                    return
                if self._balance - amount >= 0:  
                    self._balance -= amount
                    self._update_balance() 
                    self._record_transaction('Withdrawal', amount) 
                    print(f"Withdrew {amount}.  New balance: {self._balance}")
            else:
                print("Amount must be positive.")
        except ValueError:
            print("Please enter a valid number from the displayed list.")
        except Exception as e:
            print(f"An error occurred during your withdrawal, Kindly try again! {e}")

    def display_balance(self):
        print(f"Account {self._account_number} Balance: {self._balance}")

    def _account_exists(self):
        try:
            self.cursor.execute("SELECT FROM Accounts WHERE account_number = %s", (self._account_number,))
            return self.cursor.fetchone() is not None
        except mysql.connector.Error as e:
            print(f"An error occurred in the database, Please try again!: {e}")
            return False
    
    def _update_balance(self):
        try:
            self.cursor.execute(
                "UPDATE Accounts SET balance = %s WHERE account_number = %s",
                (self._balance, self._account_number)
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"An error occurred while updating balance: {e}")
            return False



