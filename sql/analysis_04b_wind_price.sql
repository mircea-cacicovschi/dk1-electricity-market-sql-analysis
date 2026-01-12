-- =====================================================
-- Analysis 04b: Wind speed vs price (DK1)
-- =====================================================
-- Examines how daily average wind speed relates to prices
-- Grain: one row per day per market
-- =====================================================

SELECT
    DATE(p.timestamp) AS date,
    m.market_code,
    AVG(w.wind_speed_ms) AS avg_wind_speed_ms,
    AVG(p.price_eur_mwh) AS avg_price_eur_mwh
FROM prices_hourly p
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