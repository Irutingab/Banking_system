from account import Account
import mysql.connector
class SavingsAccount(Account):
    def __init__(self, account_number, balance, interest_rate, min_balance, customer_id):
        super().__init__(account_number, int(balance), 'savings', customer_id) 
        self._interest_rate = int(interest_rate)  # Store interest rate as an integer (e.g., 5 for 5%)
        self._min_balance = int(min_balance)  

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
            amount = int(amount) 
            interest = amount * 0.05  # Calculate 5% of the withdrawal amount

            total_withdrawal = amount + interest  # The total amount to be withdrawn including the fee
            print(f"Attempting to withdraw {amount} with a fee of {interest}. Total withdrawal: {total_withdrawal}")

            if self._balance - total_withdrawal >= self._min_balance:
                self._balance -= total_withdrawal 
                self._update_balance()  # Update the database with the new balance
                self._record_transaction('Withdrawal', amount)  # Record the transaction
                print(f"Withdrew {amount}. Fee: {interest}. New balance: {self._balance}")
            else:
                print("Withdrawal denied: Insufficient funds to cover withdrawal and fee.")

        except ValueError:
            print("Invalid amount. Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred during withdrawal: {e}")

