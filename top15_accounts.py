import matplotlib.pyplot as plt
from DB import DataBaseConnection  


class TopTenAccounts:
    
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.cursor = db_connection.get_cursor()
        self.conn = db_connection.get_connection()
        self.display_top_accounts_by_transactions()

    def display_top_accounts_by_transactions(self):
        
        query = """
            SELECT account_number, COUNT(*) as transaction_count
            FROM Transactions
            GROUP BY account_number
            ORDER BY transaction_count DESC
            LIMIT 15
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if not results:
            print("No transactions found in the database.")
            return

        account_numbers = [row[0] for row in results]
        transaction_counts = [row[1] for row in results]

        plt.figure(figsize=(15, 6))
        plt.bar(account_numbers, transaction_counts, color='skyblue')
        plt.xlabel('Account Number')
        plt.ylabel('Number of Transactions')
        plt.title('Top 15 Accounts with Most Transactions')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

def main():
    db_connection = DataBaseConnection()  
    try:
        manager = TopTenAccounts(db_connection)  
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db_connection.get_cursor().close()  
        db_connection.get_connection().close()  
        print("Database connection closed.")

if __name__ == "__main__":
    main()