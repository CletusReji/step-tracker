# data_preprocessing.py
import pandas as pd

# Step 1: Load the step count data from the database
def load_data_from_db():
    import sqlite3

    # Connect to the SQLite database
    conn = sqlite3.connect('step_tracker.db')

    # Query the step count data
    query = "SELECT date, step_count FROM steps"
    df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    return df

# Step 2: Preprocess the data
def preprocess_data(df):
    # Handle missing values
    # Option 1: Fill missing step counts with the average step count
    average_steps = df['step_count'].mean()
    df['step_count'].fillna(average_steps, inplace=True)

    # Option 2: Remove rows with missing values (uncomment the line below if you prefer this)
    # df.dropna(inplace=True)

    # Convert the 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Sort the data by date
    df.sort_values(by='date', inplace=True)

    return df

# Step 3: Save the preprocessed data back to the database (optional)
def save_data_to_db(df):
    import sqlite3

    # Connect to the SQLite database
    conn = sqlite3.connect('step_tracker.db')
    cursor = conn.cursor()

    # Clear the existing data in the table (optional)
    cursor.execute('DELETE FROM steps')

    # Insert the preprocessed data back into the table
    df.to_sql('steps', conn, if_exists='append', index=False)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Step 4: Main function to run the preprocessing
def main():
    # Load the data from the database
    df = load_data_from_db()

    # Preprocess the data
    df = preprocess_data(df)

    # Save the preprocessed data back to the database (optional)
    save_data_to_db(df)

    # Display the preprocessed data
    print("Preprocessed Data:")
    print(df)

# Run the program
if __name__ == "__main__":
    main()