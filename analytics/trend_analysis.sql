
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


SELECT
    g.zone_name,
    ROUND(CORR(r.temperature, r.load_percentage)::numeric, 3) AS temp_load_correlation,
    COUNT(*) AS sample_size
FROM grid_readings r
JOIN grids g ON r.grid_id = g.grid_id
GROUP BY g.zone_name
HAVING COUNT(*) >= 5  -- ignore zones with too few readings to mean anything
ORDER BY temp_load_correlation DESC;