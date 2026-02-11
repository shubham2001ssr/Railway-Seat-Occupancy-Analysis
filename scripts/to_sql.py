import pandas as pd
import sqlite3
import os

# Configuration
CSV_FILE = os.path.join(os.path.dirname(__file__), "../data/railway_booking_data.csv")
DB_FILE = os.path.join(os.path.dirname(__file__), "../data/railway.db")

def load_to_sql():
    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found.")
        return

    print(f"Reading {CSV_FILE}...")
    df = pd.read_csv(CSV_FILE)
    
    # Ensure Date is datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    print(f"Connecting to {DB_FILE}...")
    conn = sqlite3.connect(DB_FILE)
    
    print("Writing to database...")
    df.to_sql('bookings', conn, if_exists='replace', index=False)
    
    # Create indexes for faster querying
    print("Creating indexes...")
    conn.execute("CREATE INDEX idx_date ON bookings (Date)")
    conn.execute("CREATE INDEX idx_train ON bookings (Train_ID)")
    conn.execute("CREATE INDEX idx_class ON bookings (Class)")
    
    conn.close()
    print("Success! Data loaded into SQLite database.")

if __name__ == "__main__":
    load_to_sql()
