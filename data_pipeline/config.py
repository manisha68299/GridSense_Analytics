
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the project root regardless of what directory
# this script is run from.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# ---------------------------------------------------------
# Database config
# ---------------------------------------------------------
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "name": os.getenv("DB_NAME", "green_grid"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['name']}"
)

# ---------------------------------------------------------
# Weather API config
# ---------------------------------------------------------
WEATHER_API_BASE_URL = os.getenv(
    "WEATHER_API_BASE_URL", "https://api.open-meteo.com/v1/forecast"
)

# ---------------------------------------------------------
# Scheduling
# ---------------------------------------------------------
PIPELINE_INTERVAL_MINUTES = int(os.getenv("PIPELINE_INTERVAL_MINUTES", 5))


GRID_LOCATIONS = [
    {"grid_id": 1, "zone_name": "North Zone",   "latitude": 23.5700, "longitude": 87.3119},
    {"grid_id": 2, "zone_name": "South Zone",   "latitude": 23.4700, "longitude": 87.3119},
    {"grid_id": 3, "zone_name": "East Zone",    "latitude": 23.5204, "longitude": 87.3600},
    {"grid_id": 4, "zone_name": "West Zone",    "latitude": 23.5204, "longitude": 87.2600},
    {"grid_id": 5, "zone_name": "Central Zone", "latitude": 23.5204, "longitude": 87.3119},
]

# ---------------------------------------------------------
# Retry config (used by utils.py's retry decorator)
# ---------------------------------------------------------
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2  # doubles each retry: 2s, 4s, 8s

# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------
LOG_FILE_PATH = PROJECT_ROOT / "logs" / "pipeline.log"