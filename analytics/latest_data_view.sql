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