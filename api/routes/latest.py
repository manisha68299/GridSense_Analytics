"""
routes/latest.py — GET /latest
Returns the current snapshot of every zone. Powers the dashboard's
KPI cards and the "current status" table. Pulls straight from
latest_data_view (Step 4) so the "what counts as latest" logic
lives in exactly one place — the SQL view, not duplicated here.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from api.database import get_db_connection
from api.schemas import LatestReading

router = APIRouter()


@router.get("/latest", response_model=list[LatestReading])
def get_latest_readings(connection=Depends(get_db_connection)):
    result = connection.execute(text("SELECT * FROM latest_data_view ORDER BY zone_name"))
    rows = result.mappings().all()
    return [LatestReading.model_validate(dict(row)) for row in rows]