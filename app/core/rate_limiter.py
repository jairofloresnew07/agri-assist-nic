import time
from collections import defaultdict
from app.core.logging import get_logger

logger = get_logger(__name__)

# Stores timestamps of recent requests per phone number
_request_log: dict[str, list[float]] = defaultdict(list)

# Configuration
WINDOW_SECONDS = 60
MAX_REQUESTS_PER_WINDOW = 3


def is_rate_limited(phone: str) -> bool:
    """
    Return True if the phone number has exceeded the allowed request rate.
    Uses a sliding window algorithm to track requests within the last WINDOW_SECONDS.
    """
    now = time.time()
    window_start = now - WINDOW_SECONDS

    # Remove timestamps outside the current window
    _request_log[phone] = [t for t in _request_log[phone] if t > window_start]

    if len(_request_log[phone]) >= MAX_REQUESTS_PER_WINDOW:
        logger.warning(
            f"Rate limit exceeded for {phone}: "
            f"{len(_request_log[phone])} requests in the last {WINDOW_SECONDS}s"
        )
        return True

    # Record the current request
    _request_log[phone].append(now)
    return False


def seconds_until_reset(phone: str) -> int:
    """Return the number of seconds until the oldest request in the window expires."""
    if not _request_log[phone]:
        return 0
    now = time.time()
    oldest = min(_request_log[phone])
    return max(0, int(WINDOW_SECONDS - (now - oldest)))
