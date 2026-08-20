-- ==========================================================
-- critical_zone_view.sql
-- Business question: "Which zones need operator attention right
-- now?" — powers the /critical API route and the alerts table
-- widget on the dashboard.
--
-- Built on top of latest_data_view so the "critical" threshold
-- logic lives in exactly one place instead of being duplicated
-- across the API and the dashboard queries.
-- ==========================================================

CREATE OR REPLACE VIEW critical_zone_view AS
SELECT
    ldv.grid_id,
    ldv.zone_name,
    ldv.location,
    ldv.load_percentage,
    ldv.temperature,
    ldv.recorded_at,
    CASE
        WHEN ldv.load_percentage >= 90 THEN 'CRITICAL'
        WHEN ldv.load_percentage >= 85 THEN 'HIGH'
        ELSE 'WARNING'
    END AS severity
FROM latest_data_view ldv
WHERE ldv.load_percentage >= 80  -- anything below this isn't worth surfacing as "critical"
ORDER BY ldv.load_percentage DESC;

-- Usage: SELECT * FROM critical_zone_view;