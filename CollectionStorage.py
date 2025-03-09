# step_tracker.py
import sqlite3
import csv

# Step 1: Create the database and table
def create_table():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('step_tracker.db')
    cursor = conn.cursor()

    # Create a table to store step count data
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

# Step 2: Add a step count record manually
def add_step_count(date, step_count):
    # Connect to the database
    conn = sqlite3.connect('step_tracker.db')
    cursor = conn.cursor()

    # Insert the step count record
    cursor.execute('''
    INSERT INTO steps (date, step_count)
    VALUES (?, ?)
    ''', (date, step_count))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Step 3: Upload step count data from a CSV file
def upload_csv(file_path):
    # Connect to the database
    conn = sqlite3.connect('step_tracker.db')
    cursor = conn.cursor()

    # Open the CSV file
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        # Insert each row into the database
        for row in reader:
            date = row[0]
            step_count = int(row[1])
            cursor.execute('''
            INSERT INTO steps (date, step_count)
            VALUES (?, ?)
            ''', (date, step_count))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Step 4: Fetch and display all step count records
def fetch_step_counts():
    # Connect to the database
    conn = sqlite3.connect('step_tracker.db')
    cursor = conn.cursor()

    # Fetch all step count records
    cursor.execute('SELECT * FROM steps')
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Display the records
    for row in rows:
        print(row)

# Step 5: Main function to run the program
def main():
    # Create the table (if it doesn't already exist)
    create_table()

    # Example: Add a step count manually
    add_step_count('2023-10-01', 7500)

    # Example: Upload step count data from a CSV file
    upload_csv('steps_data.csv')  # Replace 'steps.csv' with the path to your CSV file

    # Fetch and display all step count records
    print("Step Count Records:")
    fetch_step_counts()

# Run the program
if __name__ == "__main__":
    main()