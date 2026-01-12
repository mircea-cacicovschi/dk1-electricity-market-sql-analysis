-- =====================================================
-- Analysis 01: Hourly market overview (DK1)
-- =====================================================
-- Combines prices, load, and weather into one hourly view
-- Grain: one row per hour per market
-- =====================================================

SELECT
    p.timestamp,
    m.market_code,
    p.price_eur_mwh,
    l.load_mwh,
    w.temperature_c,
    w.wind_speed_ms
FROM prices_hourly p
JOIN load_hourly l
  ON p.timestamp = l.timestamp
 AND p.market_id = l.market_id
JOIN weather_hourly w
  ON p.timestamp = w.timestamp
 AND p.market_id = w.market_id
JOIN markets m
  ON p.market_id = m.market_id
ORDER BY p.timestamp;