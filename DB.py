import mysql.connector
import os
from dotenv import load_dotenv


env_path = os.path.join(os.path.dirname(__file__), ".env")  # Ensure correct path
load_dotenv(dotenv_path=env_path)

class DataBaseConnection:
    _instance = None  # Singleton instance

    def __new__(cls):
        """Create a single instance of the database connection."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connect()
        return cls._instance

    def connect(self):
        """Establish a database connection from the .env file."""
        try:
            db_host = os.getenv("DB_HOST")
            db_user = os.getenv("DB_USER")
            db_password = os.getenv("DB_PASSWORD")
            db_name = os.getenv("DB_NAME")

            # Check if credentials are loaded
            print(f"Loaded DB Credentials - Host: {db_host}, User: {db_user}")
            
            if not all([db_host, db_user, db_password, db_name]):
                raise ValueError("Missing database credentials. Check your .env file.")

            # Establish database connection
            self.conn = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            )
            self.cursor = self.conn.cursor()
            print("Database connection established successfully.")
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            self.conn = None
            self.cursor = None
        except ValueError as err:
            print(f"Configuration Error: {err}")

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Database connection closed.")