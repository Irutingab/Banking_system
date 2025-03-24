1. Banking System

This is a simple banking system implemented in Python. It supports basic operations for Savings and Current accounts, including deposits, withdrawals, balance checks, and interest application for savings accounts. The system also records transactions in a MySQL database.

2. Features

- Create Savings and Current accounts
- Deposit and withdraw funds
- Check account balance
- Apply interest to savings accounts
- Record transactions in a MySQL database

3. Project Structure
- env
- Databaseconnection
- account
4. Requirements

- Python 3.12+
- MySQL server
- `mysql-connector-python` library
- `python-dotenv` library


5. Project set up
- Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

- Install the required Python packages:
    ```sh
    pip install mysql-connector-python python-dotenv
    ```
- Set up the MySQL database:
    - Create a database named `banking_system`.
    - Create a table named `Transactions` with the following schema:
        ```sql
        CREATE TABLE Transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_number VARCHAR(255),
            transaction_type VARCHAR(255),
            amount FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ```
-  Configure the database connection:
    - Create a `.env` file in the project root with the following content:
        ```env
        DB1_HOST=localhost
        DB1_USER=root
        DB1_PASSWORD=your_password
        DB1_NAME=banking_system
        ```
6. Run the project
- Run the `account.py` script:
    ```sh
    python account.py
    ```
- Follow the prompts to create an account and perform various operations.

 





