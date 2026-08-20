-- ==========================================================
-- overload_detection.sql
-- Business question: "Which zones are overloaded RIGHT NOW, and
-- which are spiking compared to their own recent trend?"
--
-- Two separate signals, both useful:
--   1. Absolute overload  — load_percentage crosses a hard threshold (85%).
--   2. Relative spike     — current reading is well above that zone's
--                            own rolling average, even if not "critical" yet.
--                            This catches problems early, before they
--                            cross the hard threshold.
-- ==========================================================

-- ---- Part 1: read-only detection query (what the API/dashboard shows) ----
WITH rolling AS (
    SELECT
        r.reading_id,
        r.grid_id,
        r.load_percentage,
        r.recorded_at,
        AVG(r.load_percentage) OVER (
            PARTITION BY r.grid_id
            ORDER BY r.recorded_at
            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
        ) AS rolling_avg_load,
        ROW_NUMBER() OVER (
            PARTITION BY r.grid_id ORDER BY r.recorded_at DESC
        ) AS recency_rank
    FROM grid_readings r
)
SELECT
    g.zone_name,
    rolling.reading_id,
    rolling.load_percentage,
    ROUND(rolling.rolling_avg_load, 2) AS rolling_avg_load,
    ROUND(rolling.load_percentage - rolling.rolling_avg_load, 2) AS deviation_from_avg,
    rolling.recorded_at,
    CASE
        WHEN rolling.load_percentage >= 85 THEN 'CRITICAL'
        WHEN rolling.load_percentage - rolling.rolling_avg_load >= 15 THEN 'SPIKE'
        ELSE 'NORMAL'
    END AS status
FROM rolling
JOIN grids g ON rolling.grid_id = g.grid_id
WHERE rolling.recency_rank = 1  -- only the latest reading per zone
ORDER BY rolling.load_percentage DESC;


-- ---- Part 2: write path — insert new alerts for zones currently CRITICAL ----
-- This is what the pipeline (or a scheduled job) would run after every
-- ETL cycle to actually populate critical_alerts. It only inserts an
-- alert if the SAME reading hasn't already been flagged, so re-running
-- this doesn't create duplicate alert spam.
INSERT INTO critical_alerts (grid_id, reading_id, alert_type, severity, message)
SELECT
    r.grid_id,
    r.reading_id,
    'OVERLOAD',
    'CRITICAL',
    'Load at ' || r.load_percentage || '% for grid_id ' || r.grid_id
FROM grid_readings r
WHERE r.load_percentage >= 85
  AND r.recorded_at = (
      SELECT MAX(recorded_at) FROM grid_readings r2 WHERE r2.grid_id = r.grid_id
  )
  AND NOT EXISTS (
      SELECT 1 FROM critical_alerts ca
      WHERE ca.reading_id = r.reading_id
  );