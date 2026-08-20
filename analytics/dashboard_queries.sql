-- ==========================================================
-- dashboard_queries.sql
-- Grab-bag of queries built specifically for Power BI visuals
-- in Step 6. Each one maps to a named chart/card so there's no
-- guessing which query feeds which visual later.
-- ==========================================================

-- ---- Zone comparison bar chart: avg load per zone, all-time ----
SELECT
    g.zone_name,
    ROUND(AVG(r.load_percentage), 2) AS avg_load,
    ROUND(MAX(r.load_percentage), 2) AS peak_load,
    COUNT(*) AS total_readings
FROM grid_readings r
JOIN grids g ON r.grid_id = g.grid_id
GROUP BY g.zone_name
ORDER BY avg_load DESC;


-- ---- Top overloaded zones (ranked) — for a ranked table/card ----
SELECT
    g.zone_name,
    ldv.load_percentage AS current_load,
    RANK() OVER (ORDER BY ldv.load_percentage DESC) AS overload_rank
FROM latest_data_view ldv
JOIN grids g ON g.grid_id = ldv.grid_id
ORDER BY overload_rank
LIMIT 5;


-- ---- KPI card values: total grids, avg load, highest temp, critical count ----
SELECT
    (SELECT COUNT(*) FROM grids) AS total_grids,
    (SELECT ROUND(AVG(load_percentage), 2) FROM latest_data_view) AS avg_load_now,
    (SELECT MAX(temperature) FROM latest_data_view) AS highest_temperature_now,
    (SELECT COUNT(*) FROM critical_zone_view WHERE severity = 'CRITICAL') AS critical_zone_count;


-- ---- Load trend over time (line chart) — feeds the time-series visual ----
SELECT
    g.zone_name,
    r.recorded_at,
    r.load_percentage
FROM grid_readings r
JOIN grids g ON r.grid_id = g.grid_id
ORDER BY r.recorded_at;


-- ---- Temperature vs load (scatter plot) ----
SELECT
    g.zone_name,
    r.temperature,
    r.load_percentage
FROM grid_readings r
JOIN grids g ON r.grid_id = g.grid_id;