
import pandas as pd
import sqlite3
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
DB_DIR = BASE_DIR / "data" / "processed"

# Create processed folder if missing
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "citysupply.db"

# Load datasets
routes = pd.read_csv(DATA_DIR / "da_bus_routes.csv")
journeys = pd.read_csv(DATA_DIR / "da_journey_records.csv")
summary = pd.read_csv(DATA_DIR / "da_ridership_summary.csv")

# Convert date columns
date_columns = [
    "order_date",
    "committed_delivery_date",
    "actual_delivery_date"
]

for col in date_columns:
    journeys[col] = pd.to_datetime(
        journeys[col], errors="coerce"
    )

# Connect to SQLite
connection = sqlite3.connect(DB_PATH)

# Store datasets as SQL tables
routes.to_sql("routes", connection, if_exists="replace", index=False)

journeys.to_sql("journeys", connection, if_exists="replace", index=False)

summary.to_sql("supplier_summary", connection, if_exists="replace", index=False)

print("DATABASE CREATED SUCCESSFULLY")

# Check table records
tables = ["routes", "journeys", "supplier_summary"]

for table in tables:
    result = pd.read_sql_query(
        f"SELECT COUNT(*) AS total_records FROM {table}",
        connection
    )
    print(table, ":", result.iloc[0, 0])

connection.close()

print("Database connection closed.")
