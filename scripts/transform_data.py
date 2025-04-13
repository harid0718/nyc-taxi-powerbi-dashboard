# scripts/transform_data.py
import pandas as pd
import os

# Define input and output file paths
RAW_PATH = os.path.join("data", "raw", "yellow_tripdata_2025-01.parquet")
PROCESSED_PATH = os.path.join("data", "processed", "yellow_tripdata_2025-01_cleaned.parquet")

def transform_data():
    print("📥 Reading raw data...")
    df = pd.read_parquet(RAW_PATH)

    print(f"✅ Loaded {len(df)} rows")

    # Basic cleaning
    print("🧹 Cleaning data...")

    # Remove rows with null timestamps or passenger count = 0
    df = df.dropna(subset=["tpep_pickup_datetime", "tpep_dropoff_datetime"])
    df = df[df["passenger_count"] > 0]
    df = df[df["trip_distance"] > 0]

    # Add trip duration (in minutes)
    df["trip_duration_min"] = (
        (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]).dt.total_seconds() / 60
    )

    # Remove extreme trip durations (> 3 hours)
    df = df[(df["trip_duration_min"] > 1) & (df["trip_duration_min"] <= 180)]

    print(f"🧼 Cleaned dataset has {len(df)} rows")

    print("💾 Saving processed data...")
    df.to_parquet(PROCESSED_PATH, index=False)
    print(f"✅ Saved to {PROCESSED_PATH}")

if __name__ == "__main__":
    transform_data()
