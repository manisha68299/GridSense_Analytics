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


def safe_run_pipeline() -> None:
    """
    Last line of defense. Every individual stage already handles its
    own errors (extract/transform/load all catch locally), so in
    practice this should never fire — but if something truly
    unexpected slips through (a bug, a config typo, whatever),
    this makes sure it's LOGGED instead of silently swallowed by
    APScheduler, and makes sure one bad run doesn't crash the whole
    scheduler process so the NEXT scheduled run still happens.
    """
    try:
        run_pipeline()
    except Exception as e:
        logger.error(f"UNEXPECTED pipeline crash — scheduler will retry on next interval: {e}")


def start_scheduler() -> None:
    scheduler = BlockingScheduler()

    # Run once immediately on startup so you're not staring at an
    # empty dashboard for 5 minutes waiting for the first tick.
    safe_run_pipeline()

    scheduler.add_job(
        safe_run_pipeline,
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