"""
routes/critical.py — GET /critical
Returns zones currently at 80%+ load, ranked by severity. This is
the route grid operators actually watch — it's the "what needs my
attention right now" endpoint. Pulls from critical_zone_view (Step 4).
"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from api.database import get_db_connection
from api.schemas import CriticalZone

router = APIRouter()


@router.get("/critical", response_model=list[CriticalZone])
def get_critical_zones(connection=Depends(get_db_connection)):
    result = connection.execute(text("SELECT * FROM critical_zone_view"))
    rows = result.mappings().all()
    return [CriticalZone.model_validate(dict(row)) for row in rows]