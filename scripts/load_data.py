# scripts/load_data.py
import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Load DB credentials
DB_HOST = os.getenv("PG_HOST")
DB_PORT = os.getenv("PG_PORT")
DB_NAME = os.getenv("PG_DATABASE")
DB_USER = os.getenv("PG_USER")
DB_PASS = os.getenv("PG_PASSWORD")

# Path to cleaned file
PROCESSED_FILE = os.path.join("data", "processed", "yellow_tripdata_2025-01_cleaned.parquet")

TABLE_NAME = "yellow_tripdata"

def create_table(cursor):
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            vendor_id INT,
            tpep_pickup_datetime TIMESTAMP,
            tpep_dropoff_datetime TIMESTAMP,
            passenger_count INT,
            trip_distance FLOAT,
            rate_code_id INT,
            store_and_fwd_flag TEXT,
            pu_location_id INT,
            do_location_id INT,
            payment_type INT,
            fare_amount FLOAT,
            extra FLOAT,
            mta_tax FLOAT,
            tip_amount FLOAT,
            tolls_amount FLOAT,
            improvement_surcharge FLOAT,
            total_amount FLOAT,
            congestion_surcharge FLOAT,
            airport_fee FLOAT,
            trip_duration_min FLOAT
        );
    """)

def load_data():
    print("📥 Loading cleaned data...")
    df = pd.read_parquet(PROCESSED_FILE)
    print(f"✅ Loaded {len(df)} rows")

    print("🔗 Connecting to PostgreSQL...")
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()

    create_table(cursor)
    conn.commit()

    print("📤 Inserting data into PostgreSQL...")
    from psycopg2.extras import execute_values

    # Convert DataFrame to list of tuples
    rows = [tuple(x) for x in df.to_numpy()]

    # Generate INSERT statement
    insert_query = f"""
    INSERT INTO {TABLE_NAME} (
        vendor_id, tpep_pickup_datetime, tpep_dropoff_datetime,
        passenger_count, trip_distance, rate_code_id, store_and_fwd_flag,
        pu_location_id, do_location_id, payment_type, fare_amount, extra,
        mta_tax, tip_amount, tolls_amount, improvement_surcharge,
        total_amount, congestion_surcharge, airport_fee, trip_duration_min
    ) VALUES %s
    """

# Use execute_values for efficient bulk insert
    execute_values(cursor, insert_query, rows)

    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Data load complete!")

if __name__ == "__main__":
    load_data()
