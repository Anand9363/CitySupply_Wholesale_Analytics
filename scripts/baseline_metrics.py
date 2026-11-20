
import pandas as pd
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "outputs" / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load journey dataset
journeys = pd.read_csv(DATA_DIR / "da_journey_records.csv")

# Convert date columns
date_columns = [
    "order_date",
    "committed_delivery_date",
    "actual_delivery_date"
]

for col in date_columns:
    journeys[col] = pd.to_datetime(journeys[col], errors="coerce")

# Calculate baseline metrics
total_orders = len(journeys)
otif_orders = journeys["otif"].sum()
otif_percentage = journeys["otif"].mean() * 100

total_order_value = (
    journeys["quantity_ordered"] * journeys["unit_price"]
).sum()

average_lead_time = journeys["lead_time_days"].mean()
average_defect_rate = journeys["defect_rate"].mean()

# Display results
print("CITYSUPPLY BASELINE METRICS")
print("=" * 40)

print("Total Orders:", total_orders)
print("OTIF Orders:", otif_orders)
print("OTIF Percentage:", round(otif_percentage, 2), "%")
print("Total Order Value:", round(total_order_value, 2))
print("Average Lead Time:", round(average_lead_time, 2), "days")
print("Average Defect Rate:", round(average_defect_rate, 2))

# Save results
metrics = pd.DataFrame({
    "Metric": [
        "Total Orders",
        "OTIF Orders",
        "OTIF Percentage",
        "Total Order Value",
        "Average Lead Time",
        "Average Defect Rate"
    ],
    "Value": [
        total_orders,
        otif_orders,
        round(otif_percentage, 2),
        round(total_order_value, 2),
        round(average_lead_time, 2),
        round(average_defect_rate, 2)
    ]
})

output_file = OUTPUT_DIR / "baseline_metrics.csv"
metrics.to_csv(output_file, index=False)

print("\nBaseline metrics saved to:", output_file)
