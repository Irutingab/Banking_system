1. Banking System

This is a simple banking system implemented in Python. It supports operations for Savings and Current accounts, including deposits, withdrawals, balance checks, and interest application for savings accounts. The system also records transactions in a MySQL database. Each account is uniquely identified by its `account_number`.

2. Features

- List existing accounts
- List transactions
- Create an account (Savings or Current)
- Deposit and withdraw
  - Savings Accounts: Withdrawals include a 5% fee.
  - Current Accounts: Overdraft limits are supported.
- Display balance
- Delete account
- View user's details and update them
  - Users can selectively update specific fields or leave them unchanged.
- Record transactions and save them in the database
- Apply interest to savings accounts

3. Project Structure
- `env/` - Environment configuration files
- `Databaseconnection/` - Database connection logic
- `account.py` - Base class for account operations
- `current.py` - Logic for current accounts
- `savings.py` - Logic for savings accounts
- `customer.py` - Logic for managing customer details
- `transactions.py` - Logic for recording and managing transactions
- `main.py` - Entry point for the application

4. Requirements

- Python 3.12
- MySQL server
- `mysql-connector-python` library
- `python-dotenv` library

5. Project Setup

- Clone the repository:

    bash
    git clone <repository-url>
    cd <repository-directory>
   

- Install the required Python packages:

   bash
    pip install mysql-connector-python python-dotenv
  

- Set up the MySQL database:
    - Create a database named `banking_system`.
    - Create a table named `Customers` with the following schema:
      ```sql
      CREATE TABLE Customers (
          customer_id INT AUTO_INCREMENT PRIMARY KEY,
          name VARCHAR(100) NOT NULL,
          email VARCHAR(100) UNIQUE NOT NULL,
          phone_number VARCHAR(20),
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
      ```

    - Create a table named `Accounts` with the following schema:
      ```sql
      CREATE TABLE Accounts (
          account_id INT AUTO_INCREMENT PRIMARY KEY,  
          account_number CHAR(9) UNIQUE NOT NULL,  
          customer_id INT NOT NULL,
          account_type ENUM('Savings', 'Current') NOT NULL,
          balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
          interest_rate DECIMAL(5, 2) DEFAULT NULL,  
          min_balance DECIMAL(10, 2) DEFAULT NULL,   
          overdraft_limit DECIMAL(10, 2) DEFAULT NULL, 
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
          INDEX (account_number) 
      );
      ```

    - Create a table named `Transactions` with the following schema:
      ```sql
      CREATE TABLE Transactions (
          transaction_id INT AUTO_INCREMENT PRIMARY KEY,
          account_number CHAR(9) NOT NULL,  
          transaction_type ENUM('Deposit', 'Withdrawal', 'Interest') NOT NULL,
          amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),  
          transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (account_number) REFERENCES Accounts(account_number) ON DELETE CASCADE,
          INDEX (account_number)  
      );
      ```

- Configure the database connection:
    - Create a `.env` file in the project root with the following content:
      ```env
      DB1_HOST=localhost
      DB1_USER=root
      DB1_PASSWORD=your_password
      DB1_NAME=banking_system
      ```

6. Run the Project

- Run the `main.py` script:

    ```bash
    python main.py
    ```

- Follow the prompts to create an account and perform various operations.










