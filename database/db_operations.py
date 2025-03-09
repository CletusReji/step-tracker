# database/db_operations.py
import sqlite3

# Create the database and table
def create_table():
    conn = sqlite3.connect('step_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS steps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        step_count INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Run this function once to create the table
create_table()