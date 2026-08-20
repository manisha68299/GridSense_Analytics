-- ==========================================================
-- trend_analysis.sql
-- Business question: "Does load actually track temperature the way
-- we'd expect, and which hours of the day run hottest per zone?"
-- This is what powers the scatter plot and trend line in Power BI.
-- ==========================================================

-- ---- Hourly aggregation: avg load & temp per zone, per hour ----
-- DATE_TRUNC buckets timestamps into clean hourly groups so the
-- trend line isn't noisy with every single 5-minute reading.
SELECT
    g.zone_name,
    DATE_TRUNC('hour', r.recorded_at) AS hour_bucket,
    ROUND(AVG(r.temperature), 2) AS avg_temperature,
    ROUND(AVG(r.humidity), 2) AS avg_humidity,
    ROUND(AVG(r.load_percentage), 2) AS avg_load,
    COUNT(*) AS reading_count
FROM grid_readings r
JOIN grids g ON r.grid_id = g.grid_id
GROUP BY g.zone_name, DATE_TRUNC('hour', r.recorded_at)
ORDER BY g.zone_name, hour_bucket;


-- ---- Correlation strength between temperature and load per zone ----
-- CORR() returns Pearson's r (-1 to 1). Closer to 1 means load rises
-- with temperature almost exactly as the model assumes; closer to 0
-- would mean the two aren't really moving together for that zone.
SELECT
    g.zone_name,
    ROUND(CORR(r.temperature, r.load_percentage)::numeric, 3) AS temp_load_correlation,
    COUNT(*) AS sample_size
FROM grid_readings r
JOIN grids g ON r.grid_id = g.grid_id
GROUP BY g.zone_name
HAVING COUNT(*) >= 5  -- ignore zones with too few readings to mean anything
ORDER BY temp_load_correlation DESC;