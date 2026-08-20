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