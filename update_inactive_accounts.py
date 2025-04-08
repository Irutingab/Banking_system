from DB import DataBaseConnection
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Constants
ACCOUNT_STATUS_ACTIVE = 'active'
ACCOUNT_STATUS_DISABLED = 'disabled'

def update_account_last_active(account_number, connection=None):
    close_conn = False
    try:
        if connection is None:
            db_connection = DataBaseConnection()
            cursor = db_connection.get_cursor()
            conn = db_connection.get_connection()
            close_conn = True
        else:
            cursor = connection.get_cursor()
            conn = connection.get_connection()
            
        today = datetime.now().date()
        
        cursor.execute("""
            UPDATE Accounts 
            SET last_active = %s 
            WHERE account_number = %s
        """, (today, account_number))
        
        if close_conn:
            conn.commit()
        
        return True
    except Exception as e:
        print(f"Error updating last_active for account {account_number}: {e}")
        if close_conn:
            conn.rollback()
        return False


def update_inactive_accounts():
    
    try:
        def get_current_date():
            return datetime.now().date()
        
        def update_inactive_accounts():
            
            db_connection = DataBaseConnection()  
            cursor = db_connection.get_cursor()
            conn = db_connection.get_connection()
            
            try:
                today = get_current_date()
                five_months_ago = today - relativedelta(months=5)
                two_years_ago = today - relativedelta(years=2)
                
                
                cursor.execute("DESCRIBE Accounts")
                columns = [column[0] for column in cursor.fetchall()]
                print(f"Columns in Accounts table: {columns}")
        
                activity_column = "last_active"
                query = f"""
                    SELECT account_number, {activity_column} 
                    FROM Accounts 
                    WHERE account_status = %s 
                    AND {activity_column} < %s
                """
                cursor.execute(query, (ACCOUNT_STATUS_ACTIVE, five_months_ago))
        
                accounts_disable = cursor.fetchall()
                for account in accounts_disable:
                    account_number, last_active = account
                    days_inactive = (today - last_active).days
                    print(f"Disabling account {account_number} - inactive for {days_inactive} days")
                    
                    cursor.execute("""
                        UPDATE Accounts 
                        SET account_status = %s 
                        WHERE account_number = %s
                    """, (ACCOUNT_STATUS_DISABLED, account_number))
                    
                # Identify accounts to be deleted (inactive for 2+ years)
                query = f"""
                    SELECT account_number, {activity_column} 
                    FROM Accounts 
                    WHERE {activity_column} < %s
                """
                cursor.execute(query, (two_years_ago,))
        
                accounts_to_delete = cursor.fetchall()
                for account in accounts_to_delete:
                    account_number, last_active = account
                    days_inactive = (today - last_active).days
                    print(f"Deleting account {account_number} - inactive for {days_inactive} days")
                    
                    try:
                        # Delete related transactions
                        cursor.execute("DELETE FROM Transactions WHERE account_number = %s", (account_number,))
                        
                        # Delete the account
                        cursor.execute("DELETE FROM Accounts WHERE account_number = %s", (account_number,))
                    except Exception as delete_error:
                        print(f"Error deleting account {account_number}: {delete_error}")
                        continue
                    
                conn.commit()
                print(f"Updated {len(accounts_disable)} accounts to disabled status")
                print(f"Deleted {len(accounts_to_delete)} inactive accounts")
        
            except Exception as e:

                print(f"An error occurred while updating inactive accounts: {e}")
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")

