# ai_insights.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Step 1: Load the preprocessed data from the database
def load_data_from_db():
    import sqlite3

    # Connect to the SQLite database
    conn = sqlite3.connect('step_tracker.db')

    # Query the step count data
    query = "SELECT date, step_count FROM steps"
    df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    # Convert the 'date' column to datetime format (if not already done)
    df['date'] = pd.to_datetime(df['date'])

    return df

# Step 2: Classify days as active or inactive
def classify_active_inactive_days(df):
    # Define a threshold for active days (e.g., >5000 steps)
    threshold = 5000
    df['activity'] = df['step_count'].apply(lambda x: 'Active' if x > threshold else 'Inactive')

    # Print the classification results
    print("Active vs. Inactive Days:")
    print(df[['date', 'step_count', 'activity']])

# Step 3: Predict future step counts using Linear Regression
def predict_future_steps(df):
    # Prepare the data for prediction
    df['days'] = (df['date'] - df['date'].min()).dt.days  # Convert dates to number of days
    X = df[['days']]  # Features (number of days)
    y = df['step_count']  # Target (step count)

    # Train a Linear Regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict step counts for the next 7 days
    future_days = np.arange(df['days'].max() + 1, df['days'].max() + 8).reshape(-1, 1)
    future_steps = model.predict(future_days)

    # Print the predictions
    print("\nPredicted Step Counts for the Next 7 Days:")
    for i, steps in enumerate(future_steps, start=1):
        print(f"Day {i}: {steps:.2f} steps")

# Step 4: Provide recommendations based on the data
def provide_recommendations(df):
    # Calculate weekly activity
    df['week'] = df['date'].dt.isocalendar().week  # Extract week number
    weekly_activity = df.groupby('week')['step_count'].mean()

    # Compare the current week to the previous week
    current_week = weekly_activity.iloc[-1]
    previous_week = weekly_activity.iloc[-2] if len(weekly_activity) > 1 else current_week

    # Provide recommendations
    print("\nRecommendations:")
    if current_week > previous_week:
        print("Great job! You've been more active this week compared to last week.")
    else:
        print("You’ve been less active this week compared to last week. Try to increase your activity!")

    # Check weekend activity
    df['day_of_week'] = df['date'].dt.day_name()
    weekend_activity = df[df['day_of_week'].isin(['Saturday', 'Sunday'])]['step_count'].mean()
    if weekend_activity < 5000:
        print("You’ve been less active on weekends. Try to increase your activity on weekends!")

# Step 5: Main function to run the AI-powered insights
def main():
    # Load the preprocessed data from the database
    df = load_data_from_db()

    # Classify days as active or inactive
    classify_active_inactive_days(df)

    # Predict future step counts
    predict_future_steps(df)

    # Provide recommendations
    provide_recommendations(df)

# Run the program
if __name__ == "__main__":
    main()