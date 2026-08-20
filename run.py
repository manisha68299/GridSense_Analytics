import threading
import uvicorn

from data_pipeline.scheduler import start_scheduler
from data_pipeline.logger import get_logger

logger = get_logger(__name__)


def run_scheduler_in_background() -> None:
    """
    daemon=True means this thread is killed automatically when the
    main program exits (Ctrl+C) — otherwise the scheduler thread
    could keep the process alive even after you've told it to stop.
    """
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    logger.info("ETL scheduler started in background thread.")


if __name__ == "__main__":
    run_scheduler_in_background()

    logger.info("Starting FastAPI server on http://127.0.0.1:8000 ...")
    uvicorn.run("api.app:app", host="127.0.0.1", port=8000, reload=False)
    # reload=False here on purpose: --reload spawns a SEPARATE subprocess,
    # which would duplicate the scheduler thread. Use `uvicorn api.app:app
    # --reload` directly (Step 5's method) when you're actively editing
    # API code; use `python run.py` for the full clean demo run.