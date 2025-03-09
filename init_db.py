# init_db.py
import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('step_tracker.db')
cursor = conn.cursor()

# Create the 'steps' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    step_count INTEGER NOT NULL
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully!")