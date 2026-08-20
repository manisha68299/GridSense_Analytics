"""
routes/history.py — GET /history
Returns raw readings over time, optionally filtered to one zone.
This is what feeds the line chart / trend view — unlike /latest,
it's meant to return many rows, not just a snapshot.

Query params:
  grid_id (optional) — filter to one zone
  limit (optional, default 100, capped at 1000) — avoid accidentally
  pulling the entire table over the wire
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from api.database import get_db_connection
from api.schemas import HistoryReading

router = APIRouter()


@router.get("/history", response_model=list[HistoryReading])
def get_history(
    grid_id: int | None = Query(default=None, description="Filter to a single grid_id"),
    limit: int = Query(default=100, le=1000, description="Max rows to return"),
    connection=Depends(get_db_connection),
):
    base_query = """
        SELECT r.reading_id, r.grid_id, g.zone_name, r.temperature,
               r.humidity, r.load_percentage, r.recorded_at
        FROM grid_readings r
        JOIN grids g ON r.grid_id = g.grid_id
    """

    params = {"limit": limit}

    if grid_id is not None:
        base_query += " WHERE r.grid_id = :grid_id"
        params["grid_id"] = grid_id

    base_query += " ORDER BY r.recorded_at DESC LIMIT :limit"

    result = connection.execute(text(base_query), params)
    rows = result.mappings().all()
    return [HistoryReading.model_validate(dict(row)) for row in rows]