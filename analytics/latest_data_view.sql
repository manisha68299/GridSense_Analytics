-- ==========================================================
-- latest_data_view.sql
-- Business question: "What is the current snapshot of every zone,
-- right now?" — this is what the /latest API route and the
-- dashboard's KPI cards query directly, so it needs to be fast
-- and always return exactly one row per grid.
--
-- DISTINCT ON (Postgres-specific) grabs the single most recent
-- row per grid_id in one pass — cleaner than a window function +
-- WHERE recency_rank = 1 for this simple "latest only" case.
-- ==========================================================

CREATE OR REPLACE VIEW latest_data_view AS
SELECT DISTINCT ON (g.grid_id)
    g.grid_id,
    g.zone_name,
    g.location,
    g.max_capacity,
    r.temperature,
    r.humidity,
    r.load_percentage,
    r.recorded_at
FROM grids g
JOIN grid_readings r ON r.grid_id = g.grid_id
ORDER BY g.grid_id, r.recorded_at DESC;

-- Usage: SELECT * FROM latest_data_view;