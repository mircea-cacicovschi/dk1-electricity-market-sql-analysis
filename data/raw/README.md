## Raw data

This folder contains raw, hourly time series used in the SQL analysis.

### Data sources
- Electricity prices and load: ENTSO-E Transparency Platform
- Weather data (temperature, wind): Danish Meteorological Institute (DMI)

### Files (not tracked in git)
- `dk1_hourly_prices.csv`
- `dk1_hourly_load.csv`
- `dk1_hourly_temperature.csv`
- `dk1_hourly_wind.csv`

### Notes
- CSV files are excluded from version control due to size.
- All raw data can be regenerated using the scripts in `/scripts`.
- Time coverage: 2023-01-01 to 2025-12-31 (hourly).