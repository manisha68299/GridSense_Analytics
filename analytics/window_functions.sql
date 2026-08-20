
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