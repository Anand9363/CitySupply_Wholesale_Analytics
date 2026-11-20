
# CitySupply Wholesale Analytics
# Week 1 - Day 1
# Data Loading and Understanding

import pandas as pd
import matplotlib.pyplot as plt


# Load datasets
routes = pd.read_csv("data/da_bus_routes.csv")

journeys = pd.read_csv("data/da_journey_records.csv")

summary = pd.read_csv("data/da_ridership_summary.csv")

# Convert date columns into datetime

date_columns = [
    "order_date",
    "committed_delivery_date",
    "actual_delivery_date"
]

for col in date_columns:
    journeys[col] = pd.to_datetime(journeys[col])

print(journeys[date_columns].dtypes)

# 1. Display dataset dimensions

print("\n--- DATASET DIMENSIONS ---")

print("Routes:", routes.shape)
print("Journeys:", journeys.shape)
print("Summary:", summary.shape)


# 2. Display first five records

print("\n--- ROUTES DATA ---")
print(routes.head())

print("\n--- JOURNEYS DATA ---")
print(journeys.head())

print("\n--- SUMMARY DATA ---")
print(summary.head())


# 3. Display column names

print("\n--- COLUMN NAMES ---")

print("Routes:", routes.columns.tolist())

print("Journeys:", journeys.columns.tolist())

print("Summary:", summary.columns.tolist())


# 4. Check data types

print("\n--- JOURNEYS INFORMATION ---")

journeys.info()


# 5. Check missing values

print("\n--- MISSING VALUES ---")

print("Routes:\n", routes.isnull().sum())

print("Journeys:\n", journeys.isnull().sum())

print("Summary:\n", summary.isnull().sum())


# 6. Check duplicate records

print("\n--- DUPLICATE RECORDS ---")

print("Routes:", routes.duplicated().sum())

print("Journeys:", journeys.duplicated().sum())

print("Summary:", summary.duplicated().sum())


# 7. Statistical summary

print("\n--- STATISTICAL SUMMARY ---")

print(journeys.describe())

print("\nDay 1 data inspection completed!")


print("\n--- UNIQUE IDENTIFIERS ---")

print("Unique Routes:", routes["route_id"].nunique())

print("Unique Suppliers:", routes["supplier_id"].nunique())

print("Unique Journey Records:", journeys["record_id"].nunique())

print("Unique Purchase Orders:", journeys["po_number"].nunique())

# Check whether journey route IDs exist in routes

missing_routes = journeys[
    ~journeys["route_id"].isin(routes["route_id"])
]

print("Invalid Route IDs:", len(missing_routes))


# Check whether journey supplier IDs exist in routes

missing_suppliers = journeys[
    ~journeys["supplier_id"].isin(routes["supplier_id"])
]

print("Invalid Supplier IDs:", len(missing_suppliers))

invalid_quantity = journeys[
    journeys["quantity_delivered"] >
    journeys["quantity_ordered"]
]

print("Invalid Quantity Records:", len(invalid_quantity))


expected_otif = (
    journeys["is_on_time"] *
    journeys["is_in_full"]
)

print(
    "OTIF Mismatches:",
    (journeys["otif"] != expected_otif).sum()
)

print("First Order Date:",
      journeys["order_date"].min())

print("Last Order Date:",
      journeys["order_date"].max())

print("Number of Months:",
      summary["month_year"].nunique())

print("Available Months:")
print(sorted(summary["month_year"].unique()))

# Calculate actual delivery variance

journeys["calculated_variance"] = (
    journeys["actual_delivery_date"] -
    journeys["committed_delivery_date"]
).dt.days

# Compare calculated and existing variance

journeys["variance_mismatch"] = (
    journeys["calculated_variance"] !=
    journeys["variance_days"]
)

print("Variance mismatches:",
      journeys["variance_mismatch"].sum())

journeys["order_value"] = (
    journeys["quantity_ordered"] *
    journeys["unit_price"]
)

print("Total Order Value:",
      journeys["order_value"].sum())

total_orders = len(journeys)

otif_orders = journeys["otif"].sum()

otif_percentage = (
    otif_orders / total_orders
) * 100

print("Total Orders:", total_orders)

print("OTIF Orders:", otif_orders)

print("OTIF Percentage:", round(otif_percentage, 2))

supplier_performance = (
    journeys.groupby("supplier_id")
    .agg(
        total_orders=("po_number", "count"),
        avg_lead_time=("lead_time_days", "mean"),
        avg_defect_rate=("defect_rate", "mean"),
        otif_rate=("otif", "mean")
    )
    .reset_index()
)

supplier_performance["otif_rate"] *= 100

print(supplier_performance)

plt.figure(figsize=(11, 6))

bars = plt.bar(
    supplier_performance["supplier_id"],
    supplier_performance["otif_rate"]
)

plt.title("Supplier OTIF Performance")
plt.xlabel("Supplier ID")
plt.ylabel("OTIF Percentage")

plt.ylim(0, 115)

plt.bar_label(
    bars,
    fmt="%.1f%%",
    padding=3
)

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

supplier_value = (
    journeys.groupby("supplier_id")
    .apply(
        lambda x: (
            x["quantity_ordered"] *
            x["unit_price"]
        ).sum(),
        include_groups=False
    )
    .reset_index(name="total_order_value")
)

print(supplier_value.sort_values(
    "total_order_value",
    ascending=False
))

print(
    supplier_performance.sort_values(
        "avg_lead_time",
        ascending=False
    )
)

category_orders = (
    journeys.groupby("product_category")
    .size()
    .reset_index(name="total_orders")
)

print(category_orders.sort_values(
    "total_orders",
    ascending=False
))

attention = supplier_performance[
    supplier_performance["otif_rate"] < 70
]

print(attention)