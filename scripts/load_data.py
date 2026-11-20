
import pandas as pd
from pathlib import Path

# STEP 1: Get project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# STEP 2: Dataset directory
DATA_DIR = BASE_DIR / "data" / "raw"

# STEP 3: Create a reusable loading function
def load_datasets():

    print("CITYSUPPLY DATA PIPELINE")
    print("=" * 40)

    # Load Routes
    routes_path = DATA_DIR / "da_bus_routes.csv"
    routes = pd.read_csv(routes_path)

    # Load Journeys
    journeys_path = DATA_DIR / "da_journey_records.csv"
    journeys = pd.read_csv(journeys_path)

    # Load Summary
    summary_path = DATA_DIR / "da_ridership_summary.csv"
    summary = pd.read_csv(summary_path)

    # STEP 4: Convert date columns
    date_columns = [
        "order_date",
        "committed_delivery_date",
        "actual_delivery_date"
    ]

    for col in date_columns:
        journeys[col] = pd.to_datetime(
            journeys[col],
            errors="coerce"
        )

    # STEP 5: Display dataset dimensions
    print("\nDATASET DIMENSIONS")

    print("Routes:", routes.shape)
    print("Journeys:", journeys.shape)
    print("Summary:", summary.shape)

    # STEP 6: Display data types
    print("\nJOURNEY DATA TYPES")
    print(journeys.dtypes)

    # STEP 7: Check date conversion
    print("\nDATE CONVERSION CHECK")

    for col in date_columns:
        print(col, ":", journeys[col].dtype)

    print("\nAll datasets loaded successfully!")

    return routes, journeys, summary


# STEP 8: Execute pipeline
if __name__ == "__main__":

    routes, journeys, summary = load_datasets()
