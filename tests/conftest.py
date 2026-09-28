import pytest


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Clear rate limiter state between tests to avoid interference."""
    from app.core.rate_limiter import _request_log
    _request_log.clear()
    yield
    _request_log.clear()
