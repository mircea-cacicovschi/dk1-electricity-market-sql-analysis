import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET
from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------
TOKEN = os.getenv("ENTSOE_API_TOKEN")
if TOKEN is None:
    raise RuntimeError(
        "ENTSOE_API_TOKEN environment variable not set."
    )

AREA = "10YDK-1--------W"  # DK1: Western Denmark
DOCUMENT_TYPE = "A65"     # Total Load - Actual

START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2026, 1, 1)

OUTPUT_PATH = Path(
    "data/raw/dk1_hourly_load.csv"
)

# -----------------------------
# Data collection
# -----------------------------
data = []
current_date = START_DATE

while current_date < END_DATE:
    period_start = current_date.strftime("%Y%m%d%H%M")
    period_end = (current_date + timedelta(days=30)).strftime("%Y%m%d%H%M")

    url = (
    "https://web-api.tp.entsoe.eu/api?"
    f"securityToken={TOKEN}"
    f"&documentType={DOCUMENT_TYPE}"
    f"&processType=A16"
    f"&outBiddingZone_Domain={AREA}"
    f"&periodStart={period_start}"
    f"&periodEnd={period_end}"
)
    print(f"Fetching load: {period_start} → {period_end}")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Request failed for {period_start}, skipping.")
        current_date += timedelta(days=30)
        continue

    root = ET.fromstring(response.content)

    for timeseries in root.findall(".//{*}TimeSeries"):
        for period in timeseries.findall(".//{*}Period"):
            start_time_str = period.find(
                ".//{*}timeInterval/{*}start"
            ).text
            start_time = datetime.strptime(
                start_time_str, "%Y-%m-%dT%H:%MZ"
            )

            for point in period.findall(".//{*}Point"):
                position = int(point.find(".//{*}position").text) - 1
                load = float(point.find(".//{*}quantity").text)
                timestamp = start_time + timedelta(hours=position)

                data.append(
                    {
                        "timestamp": timestamp,
                        "market": "DK1",
                        "load_mwh": load,
                    }
                )

    current_date += timedelta(days=30)

# -----------------------------
# Final DataFrame
# -----------------------------
df = pd.DataFrame(data)

if df.empty:
    raise RuntimeError(
        "No load data fetched. Check API parameters or token."
    )

df = df.sort_values("timestamp").reset_index(drop=True)

# Enforce fixed analysis window
df = df[
    (df["timestamp"] >= START_DATE) &
    (df["timestamp"] < END_DATE)
].reset_index(drop=True)

# Handle duplicate timestamps by averaging
df = (
    df.groupby(["timestamp", "market"], as_index=False)
      .agg({"load_mwh": "mean"})
)

# -----------------------------
# Export
# -----------------------------
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

# -----------------------------
# Sanity checks
# -----------------------------
print("\n--- Data sanity checks ---")
print("Head:")
print(df.head(), "\n")

print("Tail:")
print(df.tail(), "\n")

print("Timestamp range:")
print(df.timestamp.min(), "→", df.timestamp.max(), "\n")

print("Missing values:")
print(df.isna().sum())