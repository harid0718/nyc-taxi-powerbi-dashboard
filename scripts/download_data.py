# scripts/download_data.py
import os
import requests

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
FILENAME = "yellow_tripdata_2025-01.parquet"
DEST_PATH = os.path.join("data", "raw", FILENAME)

def download_file():
    url = BASE_URL + FILENAME
    response = requests.get(url)
    if response.status_code == 200:
        with open(DEST_PATH, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {DEST_PATH}")
    else:
        print(f"Failed to download file: {url}")

if __name__ == "__main__":
    download_file()
