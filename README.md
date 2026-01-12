# DK1 Electricity Market – SQL Analysis

This project presents a structured SQL-based analysis of the Danish electricity market (DK1, Western Denmark) using hourly price, load, and weather data.  
The focus is on relational schema design, reproducible data pipelines, and analytical SQL queries that uncover key market dynamics.

The project is designed as a portfolio piece demonstrating practical SQL skills in an energy-market context.

---

## Project objectives

- Design a clean relational database schema for electricity market data  
- Load and validate real-world time series data  
- Perform exploratory and analytical SQL queries  
- Study relationships between prices, demand, and weather conditions  
- Identify drivers of extreme price events  

---

## Data sources

### Electricity prices and load  
Source: **ENTSO-E Transparency Platform**

- Day-ahead electricity prices (hourly)  
- Total load – actual (hourly)  

### Weather data  
Source: **Danish Meteorological Institute (DMI)**

- Hourly mean temperature  
- Hourly mean wind speed  

Weather variables are aggregated across a curated set of DK1 weather stations.

**Time coverage:** 2023-01-01 to 2025-12-31 (hourly)

Raw CSV files are intentionally excluded from version control and can be regenerated using the scripts in `/scripts`.

---

## Repository structure

~~~
.
├── data/
│   ├── metadata/        # Station lists and auxiliary metadata
│   └── raw/             # Raw CSV outputs (not tracked in git)
├── docs/
│   └── schema_erd.png   # Database schema diagram
├── scripts/             # Python data collection scripts
├── sql/                 # Schema and analysis SQL files
└── README.md
~~~

---

## Database schema

The database follows a star-like analytical design:

- `markets` – reference table (dimension)  
- `prices_hourly` – hourly electricity prices  
- `load_hourly` – hourly electricity demand  
- `weather_hourly` – hourly temperature and wind speed  

All fact tables share the composite key `(timestamp, market_id)` and reference the `markets` table via foreign keys.

An ER diagram of the schema is provided in `docs/schema_erd.png`.

---

## SQL analyses

The project includes the following analytical SQL files:

### Analysis 01 – Hourly market overview  
Combines prices, load, and weather into a single hourly view.

### Analysis 02 – Daily patterns  
Aggregates hourly data to daily averages to study trends and seasonality.

### Analysis 03 – Price vs load relationship  
Examines how electricity prices relate to system demand.

**Result:**  
Daily average prices show a weak positive correlation with load (Pearson r ≈ 0.12), indicating that demand alone does not explain price movements in DK1.

### Analysis 04 – Weather effects  
- **Temperature vs load:** strong negative correlation (r ≈ −0.59)  
- **Wind speed vs price:** strong negative correlation (r ≈ −0.55)  

These results highlight the dominant role of weather, particularly wind availability, in electricity price formation.

### Analysis 05 – Extreme price events  
Identifies high-price days and their system conditions.

**Key insight:**  
Extreme electricity prices in DK1 typically occur during periods of low wind availability, often combined with elevated demand, indicating supply-side constraints as the primary driver.

---

## Reproducibility

All data used in this project can be regenerated:

1. Set required API tokens as environment variables:
   - `ENTSOE_API_TOKEN`
   - `DMI_API_KEY`
2. Run the Python scripts in `/scripts`
3. Load the resulting CSVs into PostgreSQL using `sql/schema.sql`
4. Execute the analysis SQL files in `/sql`

No proprietary data or credentials are included in the repository.

---

## Tools used

- PostgreSQL and pgAdmin  
- Python (requests, pandas)  
- ENTSO-E Transparency Platform  
- DMI Open Data API  
- Git and GitHub  

---

## Author

**Mircea Cacicovschi**  
