from DB import DataBaseConnection
from datetime import datetime, timedelta

def update_inactive_accounts():
    """
    Updates account statuses based on inactivity:
    - Disable accounts inactive for 5+ months
    - Delete accounts inactive for 2+ years
    """
    db_connection = DataBaseConnection()
    cursor = db_connection.cursor
    conn = db_connection.conn
    
    try:
        today = datetime.now().date()
        five_months_ago = today - timedelta(days=5*30)  # Approximately 5 months
        two_years_ago = today - timedelta(days=2*365)  # 2 years
        
        # Identify accounts to be disabled (inactive for 5+ months)
        cursor.execute("""
            SELECT account_number, last_active 
            FROM Accounts 
            WHERE account_status = 'active' 
            AND last_active < %s
        """, (five_months_ago,))
        
        accounts_to_disable = cursor.fetchall()
        for account in accounts_to_disable:
            account_number, last_active = account
            days_inactive = (today - last_active).days
            print(f"Disabling account {account_number} - inactive for {days_inactive} days")
            
            cursor.execute("""
                UPDATE Accounts 
                SET account_status = 'disabled' 
                WHERE account_number = %s
            """, (account_number,))
            
        # Identify accounts to be deleted (inactive for 2+ years)
        cursor.execute("""
            SELECT account_number, last_active 
            FROM Accounts 
            WHERE last_active < %s
        """, (two_years_ago,))
        
        accounts_to_delete = cursor.fetchall()
        for account in accounts_to_delete:
            account_number, last_active = account
            days_inactive = (today - last_active).days
            print(f"Deleting account {account_number} - inactive for {days_inactive} days")
            
            # Delete related records first (transactions, etc.)
            cursor.execute("DELETE FROM Transactions WHERE account_number = %s", (account_number,))
            
            # Then delete the account
            cursor.execute("DELETE FROM Accounts WHERE account_number = %s", (account_number,))
            
        conn.commit()
        print(f"Updated {len(accounts_to_disable)} accounts to disabled status")
        print(f"Deleted {len(accounts_to_delete)} inactive accounts")
        
    except Exception as e:
        print(f"Error updating inactive accounts: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    update_inactive_accounts()
