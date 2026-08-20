-- ==========================================================
-- indexes.sql
-- Every index here targets a column you'll actually filter or
-- join on in Steps 3-5 (ETL lookups, analytics views, API routes).
-- Don't index everything blindly — each index costs write
-- performance, so only add what real queries need.
--
-- Run after insert_master_data.sql:
--   psql -U postgres -d green_grid -f indexes.sql
-- ==========================================================
 
-- Speeds up "get latest readings for a grid" — used constantly by
-- the analytics views and the /latest and /history API routes.
CREATE INDEX idx_grid_readings_grid_id ON grid_readings(grid_id);
 
-- Speeds up time-range queries (trend analysis, "last hour of data").
CREATE INDEX idx_grid_readings_recorded_at ON grid_readings(recorded_at DESC);
 
-- Composite index: most real queries filter by grid AND sort by time
-- together, so a combined index beats two separate single-column ones.
CREATE INDEX idx_grid_readings_grid_time ON grid_readings(grid_id, recorded_at DESC);
 
-- Speeds up the /critical route and the critical_zone_view.
CREATE INDEX idx_critical_alerts_grid_id ON critical_alerts(grid_id);
CREATE INDEX idx_critical_alerts_unresolved ON critical_alerts(is_resolved) WHERE is_resolved = FALSE;
 
-- Speeds up audit lookups per alert.
CREATE INDEX idx_alert_logs_alert_id ON alert_logs(alert_id);
 
