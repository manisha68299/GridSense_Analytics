from datetime import datetime
from data_pipeline.logger import get_logger

logger = get_logger(__name__)

# Baseline comfortable temperature (Celsius) — load estimate is
# built around deviation from this point.
BASELINE_TEMP_C = 25.0

# Tunable weights for the synthetic load formula.
TEMP_WEIGHT = 1.8
HUMIDITY_WEIGHT = 0.3
BASE_LOAD = 35.0  # idle/baseline grid load %


def _estimate_load_percentage(temperature: float, humidity: float) -> float:
    """
    Synthetic load model:
      load = base_load + (temp - baseline) * temp_weight + (humidity - 50) * humidity_weight
    Clamped to [5, 100] so it always looks like a plausible percentage.
    """
    raw_load = (
        BASE_LOAD
        + (temperature - BASELINE_TEMP_C) * TEMP_WEIGHT
        + (humidity - 50) * HUMIDITY_WEIGHT
    )
    return round(max(5.0, min(raw_load, 100.0)), 2)


def transform_records(raw_records: list[dict]) -> list[dict]:
    """
    Input: list of dicts from extract.py — {grid_id, zone_name, temperature, humidity}
    Output: list of dicts ready for load.py to insert into grid_readings —
            {grid_id, temperature, humidity, load_percentage, recorded_at}
    """
    transformed = []
    timestamp = datetime.utcnow()

    for record in raw_records:
        try:
            load_pct = _estimate_load_percentage(record["temperature"], record["humidity"])

            transformed.append({
                "grid_id": record["grid_id"],
                "temperature": record["temperature"],
                "humidity": record["humidity"],
                "load_percentage": load_pct,
                "recorded_at": timestamp,
            })
        except (KeyError, TypeError) as e:
            # A malformed record shouldn't crash the whole batch —
            # skip it and log which zone was affected.
            logger.error(f"Skipping malformed record for {record.get('zone_name', 'UNKNOWN')}: {e}")

    logger.info(f"Transformed {len(transformed)}/{len(raw_records)} records successfully.")
    return transformed


if __name__ == "__main__":
    # Quick manual test with fake extract output
    sample = [{"grid_id": 1, "zone_name": "North Zone", "temperature": 38.2, "humidity": 55}]
    print(transform_records(sample))