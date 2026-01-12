-- =====================================================
-- Analysis 04a: Temperature vs load (DK1)
-- =====================================================
-- Examines how daily average temperature relates to demand
-- Grain: one row per day per market
-- =====================================================

SELECT
    DATE(p.timestamp) AS date,
    m.market_code,
    AVG(w.temperature_c) AS avg_temperature_c,
    AVG(l.load_mwh)      AS avg_load_mwh
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
ORDER BY
    date;