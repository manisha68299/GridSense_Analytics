import requests
from data_pipeline.config import WEATHER_API_BASE_URL, GRID_LOCATIONS
from data_pipeline.utils import retry_with_backoff
from data_pipeline.logger import get_logger

logger = get_logger(__name__)


@retry_with_backoff
def _fetch_weather_for_location(latitude: float, longitude: float) -> dict:
    """
    Single API call to Open-Meteo for one lat/lon pair.
    Wrapped in retry_with_backoff because network calls are the
    single flakiest part of this pipeline.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m",
        "timezone": "auto",
    }

    response = requests.get(WEATHER_API_BASE_URL, params=params, timeout=10)
    response.raise_for_status()  # raises on 4xx/5xx so retry logic can catch it

    data = response.json()

    # Validate the shape we actually need is present before trusting it.
    if "current" not in data or "temperature_2m" not in data["current"]:
        raise ValueError(f"Unexpected Open-Meteo response shape: {data}")

    return data["current"]


def extract_all_grids() -> list[dict]:
    """
    Loops over every configured grid zone and fetches its current
    weather. A failure on one grid does NOT abort the whole run —
    we log it and continue, so one bad zone doesn't take down the
    other four.
    """
    results = []

    for grid in GRID_LOCATIONS:
        try:
            current = _fetch_weather_for_location(grid["latitude"], grid["longitude"])
            results.append({
                "grid_id": grid["grid_id"],
                "zone_name": grid["zone_name"],
                "temperature": current["temperature_2m"],
                "humidity": current["relative_humidity_2m"],
            })
            logger.info(f"Extracted weather for {grid['zone_name']} (grid_id={grid['grid_id']})")
        except Exception as e:
            logger.error(f"Failed to extract weather for {grid['zone_name']}: {e}")

    if not results:
        logger.warning("Extract stage returned zero records — check API connectivity.")

    return results


if __name__ == "__main__":
    # Quick manual test: python -m data_pipeline.extract
    data = extract_all_grids()
    for row in data:
        print(row)