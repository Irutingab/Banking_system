1. Banking System

This is a simple banking system implemented in Python. It supports operations for Savings and Current accounts, including deposits, withdrawals, balance checks, and interest application for savings accounts. The system also records transactions in a MySQL database. Each account is uniquely identified by its "account_number".

2. Requirements

- Install Python 3.12: [Download Python](https://www.python.org/downloads/)
- Install MySQL server: [Download MySQL](https://dev.mysql.com/downloads/)
- Install required Python libraries:
  - Install `mysql-connector-python`:
    ```bash
    pip install mysql-connector-python
    ```
  - Install `python-dotenv`:
    ```bash
    pip install python-dotenv
    ```
  - Install `faker`:
    ```bash
    pip install faker
    ```
  - Install `queue`:
    ```bash
    pip install queue
    ```

3. Project Setup

Step 1: Clone the Repository
- Clone the repository and navigate to the project directory:
  ```bash
  git clone <repository-url>
  cd <repository-directory>
  ```

 Step 2: Set Up the MySQL Database
- Create a database named "banking_system":
  ```sql
  CREATE DATABASE banking_system;
  ```

 Step 3: Create Database Tables
- Use the following function to create the required tables in the database:
  ```python
  from DB import DataBaseConnection

  def create_tables(db_connection):
      """
      Creates the required tables for the banking system in the database.
      """
      cursor = db_connection.get_cursor()
      try:
          # Create Customers table
          cursor.execute("""
              CREATE TABLE IF NOT EXISTS Customers (
                  customer_id INT AUTO_INCREMENT PRIMARY KEY,
                  name VARCHAR(100) NOT NULL,
                  email VARCHAR(100) UNIQUE NOT NULL,
                  phone_number VARCHAR(20) NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
              );
          """)

          # Create Accounts table
          cursor.execute("""
              CREATE TABLE IF NOT EXISTS Accounts (
                  account_id INT AUTO_INCREMENT PRIMARY KEY,
                  account_number CHAR(9) UNIQUE NOT NULL,
                  customer_id INT NOT NULL,
                  account_type ENUM('Savings', 'Current') NOT NULL,
                  balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                  interest_rate DECIMAL(5, 2) DEFAULT NULL,
                  min_balance DECIMAL(10, 2) DEFAULT NULL,
                  overdraft_limit DECIMAL(10, 2) DEFAULT NULL,
                  account_status ENUM('active', 'disactivated') NOT NULL DEFAULT 'active',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
                  INDEX (account_number)
              );
          """)

          # Create Transactions table
          cursor.execute("""
              CREATE TABLE IF NOT EXISTS Transactions (
                  transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                  account_number CHAR(9) NOT NULL,
                  transaction_type ENUM('Deposit', 'Withdrawal', 'Interest') NOT NULL,
                  amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
                  transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (account_number) REFERENCES Accounts(account_number) ON DELETE CASCADE,
                  INDEX (account_number)
              );
          """)

          db_connection.get_connection().commit()
          print("Tables created successfully.")
      except Exception as e:
          print(f"An error occurred while creating tables: {e}")
          db_connection.get_connection().rollback()
      finally:
          cursor.close()

  def setup_database():
      db_connection = DataBaseConnection()
      create_tables(db_connection)
      db_connection.get_cursor().close()
      db_connection.get_connection().close()
      print("Database setup completed.")

  if __name__ == "__main__":
      setup_database()
  ```

 Step 4: Run the Project
- Run the "main.py" script to start the application:
  ```bash
  python main.py
  ```

- Follow the prompts to perform various operations.
