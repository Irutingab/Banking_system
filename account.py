import mysql.connector 
from DB import DataBaseConnection

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
            
    def _record_transaction(self, transaction_type, amount):
        if not self._account_exists():
            print(f"Account {self._account_number} does not exist in the database.")
            return
        try:
            self.cursor.execute(
                """
                INSERT INTO Transactions (account_number, transaction_type, amount)
                VALUES (%s, %s, %s)
                """,
                (self._account_number, transaction_type, amount)
            )
            self.conn.commit()
            print("Transaction preceeded successfully")
        except mysql.connector.Error as e:
            print(f"Database error while saving transaction: {e}")


    def deposit(self, amount):
        try:
            amount = int(amount)
            if amount > 0:
                if not self._account_exists():
                    print(f"Account {self._account_number} does not exist.")
                    return
                balance_before = self._balance
                self._balance += amount
                self._update_balance()  # Update the database with the new balance
                self._record_transaction('Deposit', amount)  # save the transaction
                print(f"Deposited {amount}. Previous balance: {balance_before}, New balance: {self._balance}")
            else:
                print("Amount must be positive.")
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred during your deposit, Kindly try again! {e}")

    def withdraw(self, amount):
        try:
            amount = int(amount)
            if amount > 0:
                if not self._account_exists():
                    print(f"Account {self._account_number} does not exist.")
                    return
                if self._balance - amount >= 0:  # Ensure enough funds
                    self._balance -= amount
                    self._update_balance()  # Update the balance in the same account
                    self._record_transaction('Withdrawal', amount)  # save the transaction
                    print(f"Withdrew {amount}.  New balance: {self._balance}")
                else:
                    print("Insufficient funds.")
            else:
                print("Amount must be positive.")
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred during your withdrawal, Please try again! {e}")

    def display_balance(self):
        print(f"Account {self._account_number} Balance: {self._balance}")

    def _account_exists(self):
        try:
            self.cursor.execute("SELECT 1 FROM Accounts WHERE account_number = %s", (self._account_number,))
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
            print(f"Database updated: New balance for account {self._account_number} is {self._balance}")
        except mysql.connector.Error as e:
            print(f"Database error while updating balance: {e}")

