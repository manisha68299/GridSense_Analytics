-- ==========================================================
-- window_functions.sql
-- Business question: "What's the trending load per zone, smoothed
-- over its last 5 readings, instead of reacting to one noisy spike?"
--
-- ROWS BETWEEN 4 PRECEDING AND CURRENT ROW = a 5-reading rolling
-- window per grid. At a 5-minute polling interval that's roughly
-- the last 25 minutes of trend per zone.
-- ==========================================================

SELECT
    g.zone_name,
    r.reading_id,
    r.recorded_at,
    r.load_percentage,
    ROUND(
        AVG(r.load_percentage) OVER (
            PARTITION BY r.grid_id
            ORDER BY r.recorded_at
            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
        ), 2
    ) AS rolling_avg_load,
    -- Also rank each reading within its own grid by recency —
    -- useful later for grabbing "the last N readings" without a subquery.
    ROW_NUMBER() OVER (
        PARTITION BY r.grid_id
        ORDER BY r.recorded_at DESC
    ) AS recency_rank
FROM grid_readings r
JOIN grids g ON r.grid_id = g.grid_id
ORDER BY g.zone_name, r.recorded_at DESC;