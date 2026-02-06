import pyodbc
import os
import time

# Settings
SERVER = os.environ.get('DB_HOST', 'localhost')
USER = os.environ.get('DB_USER', 'sa')
PASSWORD = os.environ.get('DB_PASSWORD', 'YourStrong!PassWord')
DATABASE = os.environ.get('DB_NAME', 'AI_Recruiter_DB')
DRIVER = 'ODBC Driver 17 for SQL Server'

def reset_database():
    conn_str = f'DRIVER={{{DRIVER}}};SERVER={SERVER};UID={USER};PWD={PASSWORD};TrustServerCertificate=yes;Autocommit=True'
    try:
        print(f"Connecting to {SERVER}...")
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()
        
        # Kill active connections to the DB to allow Drop
        kill_query = f"""
        DECLARE @kill VARCHAR(8000) = '';
        SELECT @kill = @kill + 'kill ' + CONVERT(VARCHAR(5), session_id) + ';'
        FROM sys.dm_exec_sessions
        WHERE database_id = db_id('{DATABASE}')
        EXEC(@kill);
        """
        try:
            cursor.execute(kill_query)
        except Exception as e:
            print(f"Warning explicitly killing sessions: {e}")
        
        # Drop DB
        print(f"Dropping database {DATABASE}...")
        cursor.execute(f"IF EXISTS (SELECT name FROM sys.databases WHERE name = N'{DATABASE}') DROP DATABASE {DATABASE}")
        
        # Wait a sec
        time.sleep(2)
        
        # Create DB
        print(f"Creating database {DATABASE}...")
        cursor.execute(f"CREATE DATABASE {DATABASE}")
        print("Database reset successfully.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error resetting database: {e}")

if __name__ == "__main__":
    reset_database()
