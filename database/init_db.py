import sqlite3
import os

def init_db():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = 'docuflow.db'
    schema_path = os.path.join(current_dir, 'schema.sql')
    
    print(f"Initializing database at {db_path}...")
    try:
        conn = sqlite3.connect(db_path)
        with open(schema_path, 'r') as f:
            conn.executescript(f.read())
        conn.close()
        print(f"Database initialized successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    init_db()
