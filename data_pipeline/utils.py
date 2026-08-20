"""
utils.py — shared helpers used across the pipeline.
Currently just the retry decorator, but this is the right home
for anything reusable that isn't specific to extract/transform/load.
"""

import time
import functools
from data_pipeline.config import MAX_RETRIES, RETRY_BACKOFF_SECONDS


def retry_with_backoff(func):
    """
    Retries a function on exception, with exponential backoff.
    Use this on anything that talks to a flaky external resource —
    an API call or a DB write — not on pure in-memory logic like
    transform.py, which should fail fast if the math is wrong.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        last_exception = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < MAX_RETRIES:
                    wait_time = RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1))
                    print(
                        f"[retry] {func.__name__} failed on attempt {attempt}/{MAX_RETRIES} "
                        f"({e}). Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
        # All retries exhausted — re-raise so the caller (and logger) knows it truly failed.
        raise last_exception

    return wrapper