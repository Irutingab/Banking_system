import datetime
from collections import deque
from DB import DataBaseConnection
from mysql.connector import Error

class DatabaseUpdater:
    def __init__(self):
        self.db_connection = DataBaseConnection()
        self.conn = self.db_connection.get_connection()
        self.cursor = self.db_connection.get_cursor()
        self._queue = deque()
    
def set_to_inactive(account):
    today = datetime.date.today()
    reference_date = account.get('transaction_date') or account['created_at'].date()
    months_count = (today.year - reference_date.year) * 12 + today.month - reference_date.month
    return months_count >= 5

def set_to_delete(account):
    today = datetime.date.today()

    reference_date = account.get('transaction_date') or account['created_at'].date()
    years_count= today.year - reference_date.year
    return years_count >= 2

def process_accounts(queue, cursor, conn):
    for account in queue:
        try:
            if set_to_delete(account):
                cursor.execute("DELETE FROM Accounts WHERE account_number = %s", (account['account_number'],))
                conn.commit()
            elif set_to_inactive(account):
                cursor.execute("UPDATE Accounts SET account_status = 'inactive' WHERE account_number = %s", (account['account_number'],))
                conn.commit()
            else:
                cursor.execute("UPDATE Accounts SET account_status = 'active' WHERE account_number = %s", (account['account_number'],))
                conn.commit()
                
        except Error as e:
            print(f"An error occurred while processing account_status {account['account_number']}: {e}")
            conn.rollback()

def main():
    updater = DatabaseUpdater()
    updater.cursor.execute(
        "SELECT a.account_number, a.created_at, MAX(t.transaction_date) AS transaction_date "
        "FROM Accounts a LEFT JOIN Transactions t ON a.account_number = t.account_number "
        "GROUP BY a.account_number"
    )
    accounts = updater.cursor.fetchall()
    columns = [desc[0] for desc in updater.cursor.description]  
    account_dicts = [dict(zip(columns, account)) for account in accounts] 
    updater._queue.extend(account_dicts)
    process_accounts(updater._queue, updater.cursor, updater.conn)
    updater.conn.close()
    updater.cursor.close()
    print("Database connection closed.") 
if __name__ == "__main__":
    main()