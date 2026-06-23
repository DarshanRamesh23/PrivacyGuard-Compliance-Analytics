import pandas as pd
import sqlite3

# Load CSV
df = pd.read_csv("data/shopEasy_raw_data.csv")

# Connect to SQLite
conn = sqlite3.connect("data/privacyguard.db")
cursor = conn.cursor()

# Create raw_transactions table
df.to_sql("raw_transactions", conn, if_exists="replace", index=False)

# Create audit_log table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        check_name TEXT,
        run_timestamp TEXT,
        total_records_checked INTEGER,
        violations_found INTEGER,
        violation_rate_percent REAL,
        article_reference TEXT
    )
""")

conn.commit()
conn.close()

print("Data loaded to SQLite successfully.")
print(f"Total records loaded: {len(df)}")