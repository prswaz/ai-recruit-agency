import sqlite3
import os

db_path = "db/jobs.sqlite"

if not os.path.exists(db_path):
    print(f"Database file not found at {db_path}")
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables found in DB:")
        for t in tables:
            print(f"- {t[0]}")
            
        # Check if users table has content if it exists
        if any(t[0] == 'users' for t in tables):
            cursor.execute("SELECT count(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"Users count: {count}")
        else:
            print("CRITICAL: 'users' table is MISSING!")
            
        conn.close()
    except Exception as e:
        print(f"Error inspecting DB: {e}")
