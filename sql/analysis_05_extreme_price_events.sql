-- =====================================================
-- Analysis 05: Extreme price events (DK1)
-- =====================================================
-- Identifies high-price days and their system conditions
-- Grain: one row per day per market
-- =====================================================

WITH daily_aggregates AS (
    SELECT
        DATE(p.timestamp) AS date,
        m.market_code,
        AVG(p.price_eur_mwh) AS avg_price_eur_mwh,
        AVG(l.load_mwh)      AS avg_load_mwh,
        AVG(w.wind_speed_ms) AS avg_wind_speed_ms
    FROM prices_hourly p
    JOIN load_hourly l
      ON p.timestamp = l.timestamp
     AND p.market_id = l.market_id
    JOIN weather_hourly w
      ON p.timestamp = w.timestamp
     AND p.market_id = w.market_id
    JOIN markets m
      ON p.market_id = m.market_id
    GROUP BY
        DATE(p.timestamp),
        m.market_code
)

SELECT
    date,
    market_code,
    avg_price_eur_mwh,
    avg_load_mwh,
    avg_wind_speed_ms
FROM daily_aggregates
ORDER BY avg_price_eur_mwh DESC
LIMIT 20;