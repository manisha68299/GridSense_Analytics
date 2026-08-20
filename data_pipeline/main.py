import time
from data_pipeline.extract import extract_all_grids
from data_pipeline.transform import transform_records
from data_pipeline.load import load_records
from data_pipeline.logger import get_logger

logger = get_logger(__name__)


def run_pipeline() -> None:
    start_time = time.time()
    logger.info("=== Pipeline run started ===")

    raw_records = extract_all_grids()
    if not raw_records:
        logger.error("Aborting run: extract stage returned no data.")
        return

    clean_records = transform_records(raw_records)
    if not clean_records:
        logger.error("Aborting run: transform stage produced no valid records.")
        return

    inserted_count = load_records(clean_records)

    duration = round(time.time() - start_time, 2)
    logger.info(
        f"=== Pipeline run finished in {duration}s | "
        f"extracted={len(raw_records)} transformed={len(clean_records)} inserted={inserted_count} ==="
    )


if __name__ == "__main__":
    run_pipeline()