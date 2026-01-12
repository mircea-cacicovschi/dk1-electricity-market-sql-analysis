import os
from dmi_open_data import DMIOpenDataClient
from datetime import datetime
from pathlib import Path
import pandas as pd

# -----------------------------
# Configuration
# -----------------------------
API_KEY = os.getenv("DMI_API_KEY")
if API_KEY is None:
    raise RuntimeError(
        "DMI_API_KEY environment variable not set."
    )

MARKET = "DK1"

START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2026, 1, 1)

STATIONS_PATH = Path("data/metadata/dk1_stations_final.csv")
OUTPUT_PATH = Path(
    "data/raw/dk1_hourly_temperature.csv"
)

# -----------------------------
# Initialize client
# -----------------------------
client = DMIOpenDataClient(api_key=API_KEY)

df_stations = pd.read_csv(STATIONS_PATH)

all_station_hourly = []

# -----------------------------
# Fetch data per station
# -----------------------------
for _, row in df_stations.iterrows():
    station_id = str(row["stationId"]).zfill(5)
    station_name = row["name"]

    print(f"Fetching temperature for: {station_name} ({station_id})")

    try:
        df_temp = client.get_observations(
            parameter="temp_mean_past1h",
            station_id=station_id,
            from_time=START_DATE,
            to_time=END_DATE,
            limit=300000,
            offset=1,
            as_df=True,
        )

        if df_temp.empty or "observed" not in df_temp.columns:
            print("  No data, skipping.")
            continue
        # onvert timestamps to timezone-naive UTC for SQL compatibility
        df_temp["observed"] = (
            pd.to_datetime(df_temp["observed"], utc=True)
                .dt.tz_convert(None)
        )
        df_temp = df_temp[["observed", "value"]]
        df_temp.rename(columns={"value": station_name}, inplace=True)
        df_temp.set_index("observed", inplace=True)

        all_station_hourly.append(df_temp)

    except Exception as e:
        print(f"  Error: {e}")
        continue

# -----------------------------
# Combine and aggregate
# -----------------------------
if not all_station_hourly:
    raise RuntimeError("No temperature data fetched.")

df_combined = pd.concat(all_station_hourly, axis=1)

# DK1-wide hourly average
df_combined["temperature_c"] = df_combined.mean(axis=1)

df_result = (
    df_combined[["temperature_c"]]
    .reset_index()
    .rename(columns={"observed": "timestamp"})
)

df_result["market"] = MARKET

# Enforce fixed analysis window
df_result = df_result[
    (df_result["timestamp"] >= START_DATE)
    & (df_result["timestamp"] < END_DATE)
].reset_index(drop=True)

# -----------------------------
# Export
# -----------------------------
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df_result.to_csv(OUTPUT_PATH, index=False)

# -----------------------------
# Sanity checks
# -----------------------------
print("\n--- Data sanity checks ---")
print("Head:")
print(df_result.head(), "\n")

print("Tail:")
print(df_result.tail(), "\n")

print("Timestamp range:")
print(df_result.timestamp.min(), "→", df_result.timestamp.max(), "\n")

print("Missing values:")
print(df_result.isna().sum())