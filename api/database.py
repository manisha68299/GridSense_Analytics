"""
database.py — one shared SQLAlchemy engine + a FastAPI dependency
that hands each request a connection and closes it afterward.

Reuses the same DATABASE_URL config as the ETL pipeline, so there's
only ever one place credentials are defined for the whole project.
"""

from sqlalchemy import create_engine
from data_pipeline.config import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def get_db_connection():
    """
    FastAPI dependency — yields a connection, guarantees it's closed
    even if the route raises an exception. Used as: Depends(get_db_connection)
    """
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()