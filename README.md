1. Banking System

This is a simple banking system implemented in Python. It supports operations for Savings and Current accounts, including deposits, withdrawals, balance checks, and interest application for savings accounts. The system also records transactions in a MySQL database. Each account is uniquely identified by its "account_number".

2. Features
- add a user/customer
- Create an account (Savings or Current): an account is assigned to an existing user/customer
- Deposit and withdraw
  - Savings Accounts: Withdrawals include a 5% interest of the withdrawed amount.
  - Current Accounts: Overdraft limits are supported.

- Delete accounts
  - Accounts are automatically set to *deleted* after two years of inactivity  

- Deactivate accounts
  - Accounts are automatically deactivated or set to *Inactive*after five months of inactivity.
- View user's/customer's details and update them

  - Users can selectively update specific fields or leave them unchanged.
- Record transactions and save them in the database
- Apply interest to savings accounts
- Edit account's specificities
   - Savings accounts: update interest_rate, or minimum_balance
   - Current accounts: update overdraf limits depending on how much users are deposting

3. Project Structure
- "env/" - Environment configuration files
- "Databaseconnection: DB.py/" - Database connection logic
- "account.py" - Base class for account operations
- "current.py" - Logic for current accounts
- "savings.py" - Logic for savings accounts
- "customer.py" - Logic for managing customer details
- "transactions.py" - Logic for recording and managing transactions
- "generate_fake_data" - Logic for generating random data from faker
- "account_activity" - Logic for checking if accounts are active, inactive, or deleted
- "main.py" - Entry point for the application

4. Requirements

- Python 3.12
- MySQL server
- mysql-connector-python library
- python-dotenv library
- Faker library
- queue library

5. Project Setup

- Clone the repository:

    git clone <repository-url>
    cd <repository-directory>


- Install the required packages:
  
    pip install mysql-connector-python python-dotenv faker queue


- Set up the MySQL database:
    - Create a database named "banking_system".
    
      - ```sql a table named "Customers" with the following schema:
      CREATE TABLE Customers (
          customer_id INT AUTO_INCREMENT PRIMARY KEY,
          name VARCHAR(100) NOT NULL,ENT PRIMARY KEY,
          email VARCHAR(100) UNIQUE NOT NULL,
          phone_number VARCHAR(20), NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      ```
      ```
    - 
```sql a table named "Accounts" with the following schema:
      CREATE TABLE Accounts (
          account_id INT AUTO_INCREMENT PRIMARY KEY,  
          account_number CHAR(9) UNIQUE NOT NULL,  ,  
          customer_id INT NOT NULL,IQUE NOT NULL,  
          account_type ENUM('Savings', 'Current') NOT NULL,
          balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,ULL,
          interest_rate DECIMAL(5, 2) DEFAULT NULL,  0,
          min_balance DECIMAL(10, 2) DEFAULT NULL,   
          overdraft_limit DECIMAL(10, 2) DEFAULT NULL, 
          account_status ENUM('active', 'disactivated') NOT NULL DEFAULT 'active', -- Indicates the account status
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,OT NULL DEFAULT 'active', -- Indicates the account status
          FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
          INDEX (account_number) d) REFERENCES Customers(customer_id) ON DELETE CASCADE,
      ;  INDEX (account_number) 

      
      - sql a table named "Transactions" with the following schema:
      CREATE TABLE Transactions (
          transaction_id INT AUTO_INCREMENT PRIMARY KEY,
          account_number CHAR(9) NOT NULL,  PRIMARY KEY,
          transaction_type ENUM('Deposit', 'Withdrawal', 'Interest') NOT NULL,
          amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),  rest') NOT NULL,
          transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (account_number) REFERENCES Accounts(account_number) ON DELETE CASCADE,
          INDEX (account_number)  ber) REFERENCES Accounts(account_number) ON DELETE CASCADE,
      );  INDEX (account_number)  
     
- Configure the database connection:
    - env a ".env" file in the project root with the following content:
      DB_HOST=localhost
      DB_USER=rootlhost
      DB_PASSWORD=your_password
      DB_NAME=banking_system
     
6. Run the Project
- Run the "main.py" script:

    - python main.py
    
- Follow the prompts to perform various operations.
