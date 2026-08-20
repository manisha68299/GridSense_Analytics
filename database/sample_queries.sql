SELECT r.reading_id, g.zone_name, r.temperature, r.humidity, r.load_percentage, r.recorded_at
FROM grid_readings r
JOIN grids g ON r.grid_id = g.grid_id
ORDER BY r.recorded_at DESC;