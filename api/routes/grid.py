"""
routes/grid.py — GET /grid/{id}
Returns full detail for one specific zone: its static metadata
(location, max_capacity) plus its latest reading, in a single call.
Useful for a "zone detail page" click-through in the dashboard.

LEFT JOIN (not INNER) matters here: a brand new grid with zero
readings yet should still return its metadata instead of a 404 —
only a genuinely nonexistent grid_id should 404.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from api.database import get_db_connection
from api.schemas import GridDetail

router = APIRouter()


@router.get("/grid/{grid_id}", response_model=GridDetail)
def get_grid_detail(grid_id: int, connection=Depends(get_db_connection)):
    query = text("""
        SELECT
            g.grid_id, g.zone_name, g.location, g.max_capacity, g.created_at,
            r.load_percentage AS latest_load_percentage,
            r.temperature AS latest_temperature,
            r.recorded_at AS latest_recorded_at
        FROM grids g
        LEFT JOIN LATERAL (
            SELECT load_percentage, temperature, recorded_at
            FROM grid_readings
            WHERE grid_id = g.grid_id
            ORDER BY recorded_at DESC
            LIMIT 1
        ) r ON true
        WHERE g.grid_id = :grid_id
    """)

    result = connection.execute(query, {"grid_id": grid_id})
    row = result.mappings().first()

    if row is None:
        raise HTTPException(status_code=404, detail=f"Grid with id {grid_id} not found")

    return GridDetail.model_validate(dict(row))