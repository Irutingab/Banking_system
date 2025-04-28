import mysql.connector 
from DB import DataBaseConnection

def print_first_5_accounts(cursor):
    try:
        cursor.execute(
            "SELECT account_number, account_type, customer_id "
            "FROM Accounts LIMIT 5"
        )
        accounts = cursor.fetchall()
        #print(f"[ Accountid: {account[0]}, Account Number: {account[1]},accountype: {account[2]}]")
        if accounts:
            print("First 5 accounts:")
            #print(accounts)
            accounts = [list(account) for account in accounts]
            print(accounts)
            #for account in accounts:
                #print(f"[ Accountid: {account[0]}, Account Number: {account[1]},accountype: {account[2]}]")
        else:
            print("No accounts found in the database.")
    except mysql.connector.Error as e:
        print(f"An error occurred while fetching accounts: {e}")

if __name__ == "__main__":
    db_connection = DataBaseConnection()
    cursor = db_connection.get_cursor()
    print_first_5_accounts(cursor)
    cursor.close()
    db_connection.get_connection().close()