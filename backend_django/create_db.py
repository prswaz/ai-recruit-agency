import pyodbc
import os

# Settings from settings.py defaults
SERVER = os.environ.get('DB_HOST', 'localhost')
USER = os.environ.get('DB_USER', 'sa')
PASSWORD = os.environ.get('DB_PASSWORD', 'YourStrong!PassWord')
DATABASE = os.environ.get('DB_NAME', 'AI_Recruiter_DB')
DRIVER = 'ODBC Driver 17 for SQL Server'

def create_database():
    conn_str = f'DRIVER={{{DRIVER}}};SERVER={SERVER};UID={USER};PWD={PASSWORD};TrustServerCertificate=yes;Autocommit=True'
    try:
        # Connect to master to create DB
        print(f"Connecting to {SERVER}...")
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()
        
        # Check if exists
        check_db_query = f"SELECT name FROM master.dbo.sysdatabases WHERE name = N'{DATABASE}'"
        cursor.execute(check_db_query)
        if cursor.fetchone():
            print(f"Database {DATABASE} already exists.")
        else:
            print(f"Creating database {DATABASE}...")
            cursor.execute(f"CREATE DATABASE {DATABASE}")
            print("Database created successfully.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_database()
