-- =====================================
-- Schema: Electricity Market (Hourly)
-- =====================================

-- Drop tables if they exist (for clean re-runs)
DROP TABLE IF EXISTS weather_hourly;
DROP TABLE IF EXISTS load_hourly;
DROP TABLE IF EXISTS prices_hourly;
DROP TABLE IF EXISTS markets;

-- =====================================
-- Markets
-- =====================================
CREATE TABLE markets (
    market_id SERIAL PRIMARY KEY,
    market_code TEXT NOT NULL UNIQUE,
    market_name TEXT NOT NULL
);

-- =====================================
-- Hourly Prices
-- =====================================
CREATE TABLE prices_hourly (
    timestamp TIMESTAMP NOT NULL,
    market_id INTEGER NOT NULL,
    price_eur_mwh NUMERIC(10,4) NOT NULL,
    PRIMARY KEY (timestamp, market_id),
    FOREIGN KEY (market_id) REFERENCES markets (market_id)
);

-- =====================================
-- Hourly Load
-- =====================================
CREATE TABLE load_hourly (
    timestamp TIMESTAMP NOT NULL,
    market_id INTEGER NOT NULL,
    load_mwh NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (timestamp, market_id),
    FOREIGN KEY (market_id) REFERENCES markets (market_id)
);

-- =====================================
-- Hourly Weather
-- =====================================
CREATE TABLE weather_hourly (
    timestamp TIMESTAMP NOT NULL,
    market_id INTEGER NOT NULL,
    temperature_c NUMERIC(5,2),
    wind_speed_ms NUMERIC(5,2),
    PRIMARY KEY (timestamp, market_id),
    FOREIGN KEY (market_id) REFERENCES markets (market_id)
);