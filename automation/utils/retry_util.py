"""
Retry decorator for flaky Selenium tests.
"""

import time
import functools
import traceback
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import MAX_RETRIES, RETRY_DELAY


def retry(max_retries: int = MAX_RETRIES, delay: int = RETRY_DELAY):
    """
    Decorator that retries a test function on failure.

    Args:
        max_retries: Number of retry attempts.
        delay: Seconds to wait between retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        print(
                            f"[RETRY] {func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {e}"
                        )
                        time.sleep(delay)
                    else:
                        print(
                            f"[RETRY] {func.__name__} exhausted all {max_retries + 1} attempts"
                        )
            raise last_exception
        return wrapper
    return decorator
