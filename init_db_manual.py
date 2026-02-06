import sqlite3
import os

db_path = "db/jobs.sqlite"
schema_path = "db/schema.sql"

if not os.path.exists(schema_path):
    print(f"Schema file not found at {schema_path}")
    exit(1)

print(f"Applying schema from {schema_path} to {db_path}...")

with open(schema_path, 'r') as f:
    schema = f.read()

try:
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema)
    print("Schema applied successfully.")
except Exception as e:
    print(f"Error applying schema: {e}")
