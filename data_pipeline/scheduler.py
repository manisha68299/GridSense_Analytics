"""
scheduler.py — runs the pipeline once immediately, then re-runs it
every PIPELINE_INTERVAL_MINUTES (default 5) indefinitely.

This is what makes it a "live" system instead of a one-off script —
you'd run this as a background process (or a systemd service /
Docker container in a real deployment) alongside the FastAPI server.
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from data_pipeline.main import run_pipeline
from data_pipeline.config import PIPELINE_INTERVAL_MINUTES
from data_pipeline.logger import get_logger

logger = get_logger(__name__)


def start_scheduler() -> None:
    scheduler = BlockingScheduler()

    # Run once immediately on startup so you're not staring at an
    # empty dashboard for 5 minutes waiting for the first tick.
    run_pipeline()

    scheduler.add_job(
        run_pipeline,
        "interval",
        minutes=PIPELINE_INTERVAL_MINUTES,
        id="energy_pipeline_job",
    )

    logger.info(f"Scheduler started — running every {PIPELINE_INTERVAL_MINUTES} minutes. Ctrl+C to stop.")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped by user.")


if __name__ == "__main__":
    start_scheduler()