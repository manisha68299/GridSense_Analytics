
import time
import functools
from data_pipeline.config import MAX_RETRIES, RETRY_BACKOFF_SECONDS


def retry_with_backoff(func):
    
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