import mysql.connector
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

class DataBaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = None
            cls._instance.cursor = None
            cls._instance.connect()
        return cls._instance

    def connect(self):
        try:
            db_host = os.getenv("DB_HOST")
            db_user = os.getenv("DB_USER")
            db_password = os.getenv("DB_PASSWORD")
            db_name = os.getenv("DB_NAME")

            if not all([db_host, db_user, db_password, db_name]):
                raise ValueError("A few credential are missing.")

            self.conn = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            )
            self.cursor = self.conn.cursor()
            print("DB connection successful.")
        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")

    def get_cursor(self):
        if self.cursor:
            return self.cursor
        raise ConnectionError("No cursor available.")

    def get_connection(self):
        if self.conn:
            return self.conn
        raise ConnectionError("No Database connection available.")

    def close(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Database connection closed.")
