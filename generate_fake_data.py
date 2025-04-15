from faker import Faker
import random
from datetime import datetime, timedelta
from collections import deque
from DB import DataBaseConnection

fake = Faker()

def random_date(start_year=2018):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    data = end_date - start_date
    random_days = random.randint(0, data.days)
    return start_date + timedelta(days=random_days)

def generate_rwandan_phone_number():
    return f"+2507{random.randint(0, 9)}{random.randint(1000000, 9999999)}"

def insert_batch(cursor, conn, queue, query):
    while queue:
        batch = [queue.popleft() for _ in range(min(len(queue), 1000))]#processes the data and ensures it is added to he DB in order
        cursor.executemany(query, batch)
        conn.commit()

#def generate_customers(cursor, conn, num_records=1000000):
 #   print("Generating customers")
  #  queue = deque()
   # query = "INSERT INTO Customers (name, email, phone_number) VALUES (%s, %s, %s)"
    #for _ in range(num_records):
     #   name = fake.name()
      #  email = fake.unique.email()
       # phone_number = generate_rwandan_phone_number()
        #queue.append((name, email, phone_number))
        #if len(queue) >= 1000:  
         #   insert_batch(cursor, conn, queue, query)
    #insert_batch(cursor, conn, queue, query)  
    #print(f"{num_records} customers inserted successfully.")

def get_customer_id_range(cursor):
    cursor.execute("SELECT MIN(customer_id), MAX(customer_id) FROM Customers")
    return cursor.fetchone()

def get_all_customer_ids(cursor):
    cursor.execute("SELECT customer_id FROM Customers")
    return [row[0] for row in cursor.fetchall()]  

#def generate_accounts(cursor, conn, num_records=1000000):
 #   print("Generating accounts")
  #  queue = deque()
   # query = """
    #    INSERT INTO Accounts (account_number, customer_id, account_type, balance, interest_rate, min_balance, overdraft_limit, account_status, created_at)
     #   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    #"""
    #customer_ids = get_all_customer_ids(cursor)  
    #if not customer_ids:
     #   raise ValueError("No customers found in the database")

    #Fetch valid ENUM values for account_status
    #cursor.execute("SHOW COLUMNS FROM Accounts LIKE 'account_status'")
    #account_status_enum_result = cursor.fetchone()
    #if not account_status_enum_result:
     #   raise ValueError("The 'account_status' column does not exist in the Accounts table. Please check the database schema.")

    #account_status_enum = account_status_enum_result[1]  # Extract ENUM definition
    #valid_account_statuses = account_status_enum.replace("enum(", "").replace(")", "").replace("'", "").split(",")
    #Ensure account_status has valid values
    #if not valid_account_statuses:
     #   raise ValueError("No valid account statuses found.")

    #for _ in range(num_records):
     #   account_number = fake.unique.random_number(digits=9, fix_len=True)
      #  customer_id = random.choice(customer_ids)  
       # account_type = random.choice(['Savings', 'Current'])
        #balance = round(random.uniform(0, 100000), 2)
        #interest_rate = round(random.uniform(0, 20), 2) if account_type == 'Savings' else None
        #min_balance = round(random.uniform(0, 5000), 2) if account_type == 'Savings' else None
        #overdraft_limit = round(random.uniform(0, 10000), 2) if account_type == 'Current' else None
        #account_status = random.choice(valid_account_statuses) 
        #created_at = random_date().strftime('%Y-%m-%d %H:%M:%S')
        #queue.append((account_number, customer_id, account_type, balance, interest_rate, min_balance, overdraft_limit, account_status, created_at))
        #if len(queue) >= 1000: 
            
         #   insert_batch(cursor, conn, queue, query)
          #  insert_batch(cursor, conn, queue, query) 
           # print(f"{num_records} accounts inserted successfully.")

def get_all_account_numbers(cursor):
    cursor.execute("SELECT account_number FROM Accounts")
    return [row[0] for row in cursor.fetchall()]  

def generate_transactions(cursor, conn, num_records=1000000):
    print("Generating transactions...")
    queue = deque()
    query = """
        INSERT INTO Transactions (account_number, transaction_type, amount, transaction_date)
        VALUES (%s, %s, %s, %s)
    """
    account_numbers = get_all_account_numbers(cursor)  
    if not account_numbers:
        raise ValueError("No accounts found in the database. Please generate accounts first.")

    for account_number in account_numbers:
        # Randomly decide how many transactions this account will have (0 to 30)
        num_transactions = random.randint(0, 30)
        for _ in range(num_transactions):
            transaction_type = random.choice(['Deposit', 'Withdrawal', 'Interest'])
            amount = round(random.uniform(1, 10000), 2)
            transaction_date = random_date().strftime('%Y-%m-%d %H:%M:%S')

            queue.append((account_number, transaction_type, amount, transaction_date))
            if len(queue) >= 1000: 
                insert_batch(cursor, conn, queue, query)
    insert_batch(cursor, conn, queue, query) 
    print("Transactions generated for accounts. Some accounts may have no transactions.")

def main():
    db_connection = DataBaseConnection()
    cursor = db_connection.get_cursor()
    conn = db_connection.get_connection()

    try:
        #generate_customers(cursor, conn)
        #generate_accounts(cursor, conn)
        generate_transactions(cursor, conn)
    except Exception as e:
        print(f"An error occurred while generating data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        print("DB connection closed.")

if __name__ == "__main__":
    main()
