from sqlalchemy import create_engine, text
from data_pipeline.config import DATABASE_URL
from data_pipeline.utils import retry_with_backoff
from data_pipeline.logger import get_logger

logger = get_logger(__name__)

# One engine, reused across pipeline runs, instead of reconnecting
# every 5 minutes. SQLAlchemy's connection pool handles the rest.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

INSERT_QUERY = text("""
    INSERT INTO grid_readings (grid_id, temperature, humidity, load_percentage, recorded_at)
    VALUES (:grid_id, :temperature, :humidity, :load_percentage, :recorded_at)
""")


@retry_with_backoff
def _insert_batch(connection, records: list[dict]) -> None:
    
    connection.execute(INSERT_QUERY, records)
    connection.commit()


def load_records(records: list[dict]) -> int:
    """
    Inserts a list of transformed records into grid_readings.
    Returns the number of records successfully inserted.
    """
    if not records:
        logger.warning("load_records called with an empty list — nothing to insert.")
        return 0

    try:
        with engine.connect() as connection:
            _insert_batch(connection, records)
        logger.info(f"Inserted {len(records)} records into grid_readings.")
        return len(records)
    except Exception as e:
        logger.error(f"Failed to insert records after retries: {e}")
        return 0


if __name__ == "__main__":
    # Quick manual test — only run this after Step 2's tables exist.
    from datetime import datetime
    sample = [{
        "grid_id": 1, "temperature": 36.0, "humidity": 48.0,
        "load_percentage": 41.8, "recorded_at": datetime.utcnow(),
    }]
    print(f"Inserted: {load_records(sample)}")