# trend_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# Step 2: Visualize daily step trends
def plot_daily_trends(df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='date', y='step_count', data=df, marker='o')
    plt.title('Daily Step Trends')
    plt.xlabel('Date')
    plt.ylabel('Step Count')
    plt.grid(True)
    plt.show()

# Step 3: Categorize and visualize active vs. inactive days
def plot_active_inactive_days(df):
    # Define thresholds for active and inactive days
    df['activity'] = df['step_count'].apply(lambda x: 'Active' if x > 5000 else 'Inactive')

    # Plot a bar chart
    plt.figure(figsize=(8, 5))
    sns.countplot(x='activity', data=df, palette='Set2')
    plt.title('Active vs. Inactive Days')
    plt.xlabel('Activity')
    plt.ylabel('Number of Days')
    plt.show()

    # Plot a pie chart (optional)
    activity_counts = df['activity'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(activity_counts, labels=activity_counts.index, autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'])
    plt.title('Active vs. Inactive Days')
    plt.show()

# Step 4: Calculate and visualize weekly/monthly averages
def plot_weekly_monthly_averages(df):
    # Resample data to get weekly and monthly averages
    df.set_index('date', inplace=True)
    weekly_avg = df.resample('W').mean()
    monthly_avg = df.resample('M').mean()

    # Plot weekly averages
    plt.figure(figsize=(10, 6))
    sns.barplot(x=weekly_avg.index, y='step_count', data=weekly_avg, palette='viridis')
    plt.title('Weekly Average Step Counts')
    plt.xlabel('Week')
    plt.ylabel('Average Step Count')
    plt.xticks(rotation=45)
    plt.show()

    # Plot monthly averages
    plt.figure(figsize=(10, 6))
    sns.barplot(x=monthly_avg.index, y='step_count', data=monthly_avg, palette='magma')
    plt.title('Monthly Average Step Counts')
    plt.xlabel('Month')
    plt.ylabel('Average Step Count')
    plt.xticks(rotation=45)
    plt.show()

# Step 5: Main function to run the analysis and visualization
def main():
    # Load the preprocessed data from the database
    df = load_data_from_db()

    # Visualize daily step trends
    plot_daily_trends(df)

    # Visualize active vs. inactive days
    plot_active_inactive_days(df)

    # Visualize weekly and monthly averages
    plot_weekly_monthly_averages(df)

# Run the program
if __name__ == "__main__":
    main()