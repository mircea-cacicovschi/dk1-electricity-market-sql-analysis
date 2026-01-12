-- =====================================================
-- Analysis 03: Price vs load relationship (DK1)
-- =====================================================
-- Examines how daily average prices move with demand
-- Grain: one row per day per market
-- =====================================================

SELECT
    DATE(p.timestamp) AS date,
    m.market_code,
    AVG(p.price_eur_mwh) AS avg_price_eur_mwh,
    AVG(l.load_mwh)      AS avg_load_mwh
FROM prices_hourly p
JOIN load_hourly l
  ON p.timestamp = l.timestamp
 AND p.market_id = l.market_id
JOIN markets m
  ON p.market_id = m.market_id
GROUP BY
    DATE(p.timestamp),
    m.market_code
ORDER BY
    date;