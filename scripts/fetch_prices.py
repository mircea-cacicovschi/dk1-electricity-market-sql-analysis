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
DOCUMENT_TYPE = "A44"
PROCESS_TYPE = "A01"

# Fixed analysis window: 2023–2025
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2026, 1, 1)

OUTPUT_PATH = Path(
    "data/raw/dk1_hourly_prices.csv"
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
        f"&processType={PROCESS_TYPE}"
        f"&in_Domain={AREA}"
        f"&out_Domain={AREA}"
        f"&periodStart={period_start}"
        f"&periodEnd={period_end}"
    )

    print(f"Fetching prices: {period_start} → {period_end}")
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
                price = float(point.find(".//{*}price.amount").text)
                timestamp = start_time + timedelta(hours=position)

                data.append(
                    {
                        "timestamp": timestamp,
                        "market": "DK1",
                        "price_eur_mwh": price,
                    }
                )

    current_date += timedelta(days=30)

# -----------------------------
# Final DataFrame
# -----------------------------
df = pd.DataFrame(data)
df = df.sort_values("timestamp").reset_index(drop=True)

# Enforce fixed analysis window
df = df[
    (df["timestamp"] >= START_DATE) &
    (df["timestamp"] < END_DATE)
].reset_index(drop=True)

df = (
    df.groupby(["timestamp", "market"], as_index=False)
      .agg({"price_eur_mwh": "mean"})
)

# -----------------------------
# Export
# -----------------------------
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print(f"Saved {len(df)} rows to {OUTPUT_PATH}")



print("\n--- Data sanity checks ---")
print("Head:")
print(df.head(), "\n")

print("Tail:")
print(df.tail(), "\n")

print("Timestamp range:")
print(df.timestamp.min(), "→", df.timestamp.max(), "\n")

print("Missing values:")
print(df.isna().sum())