
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

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

# 1. Missing values
print("\n--- MISSING VALUES ---")

for name, df in [
    ("Routes", routes),
    ("Journeys", journeys),
    ("Summary", summary)
]:
    print(f"\n{name}")
    print(df.isnull().sum())

# 2. Duplicate records
print("\n--- DUPLICATE RECORDS ---")

print("Routes:", routes.duplicated().sum())
print("Journeys:", journeys.duplicated().sum())
print("Summary:", summary.duplicated().sum())

# 3. Invalid quantities
print("\n--- QUANTITY VALIDATION ---")

invalid_quantity = journeys[
    (journeys["quantity_ordered"] <= 0) |
    (journeys["quantity_delivered"] < 0)
]

print("Invalid quantity records:", len(invalid_quantity))

# 4. Date validation
print("\n--- DATE VALIDATION ---")

invalid_dates = journeys[
    journeys[date_columns].isnull().any(axis=1)
]

print("Invalid date records:", len(invalid_dates))

# 5. Delivery validation
print("\n--- DELIVERY VALIDATION ---")

delivery_mismatch = journeys[
    journeys["quantity_delivered"] >
    journeys["quantity_ordered"]
]

print("Delivery quantity mismatches:", len(delivery_mismatch))

print("\nData quality inspection completed!")
