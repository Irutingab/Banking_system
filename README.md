1. Banking System

This is a simple banking system implemented in Python. It supports operations for Savings and Current accounts, including deposits, withdrawals, balance checks, and interest application for savings accounts. The system also records transactions in a MySQL database.

2. Features

- list existing accounts
- list transactions
- create an account(savings or current)
- Deposit and withdraw
- Display balance
- Delete account
- view user's details and update them 
- Record transactions and save them in the database
- Appy interest

3. Project Structure
- env
- Databaseconnection
- account

4. Requirements

- Python 3.12
- MySQL server
- mysql-connector-python library
- python-dotenv library


5. Project set up
- Clone the repository:

    git clone <repository-url>
    cd <repository-directory>

- Install the required Python packages:

    pip install mysql-connector-python python-dotenv

- Set up the MySQL database:
    - Create a database named "banking_system".
    -  Create a table named "accounts" with the following schema:
       CREATE TABLE Accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    account_type ENUM('Savings', 'Current') NOT NULL,
    balance DECIMAL(10, 2) NOT NULL,
    interest_rate DECIMAL(5, 2) DEFAULT NULL,  
    min_balance DECIMAL(10, 2) DEFAULT NULL,   
    overdraft_limit DECIMAL(10, 2) DEFAULT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
- Create a table named "customers" with the following schema:

   CREATE TABLE Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

- Create a table named "Transactions" with the following schema:
       
      CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    transaction_type ENUM('Deposit', 'Withdrawal', 'Interest') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE
);

-  Configure the database connection:
    - Create a .env file in the project root with the following content:
       "env

        DB1_HOST=localhost
        DB1_USER=root
        DB1_PASSWORD=your_password
        DB1_NAME=banking_system
        "
6. Run the project
- Run the "account.py" script:

    python account.py

- Follow the prompts to create an account and perform various operations.







