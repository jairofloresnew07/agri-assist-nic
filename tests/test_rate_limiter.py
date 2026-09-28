import time
import pytest
from app.core.rate_limiter import is_rate_limited, seconds_until_reset, _request_log


def _clear(phone: str):
    """Remove all rate limit records for a phone number."""
    _request_log.pop(phone, None)


def test_first_request_is_not_limited():
    phone = "test_first_001"
    _clear(phone)
    assert is_rate_limited(phone) is False


def test_requests_within_limit_are_allowed():
    phone = "test_within_002"
    _clear(phone)
    # First 3 requests should pass
    assert is_rate_limited(phone) is False
    assert is_rate_limited(phone) is False
    assert is_rate_limited(phone) is False


def test_fourth_request_is_blocked():
    phone = "test_fourth_003"
    _clear(phone)
    is_rate_limited(phone)  # 1
    is_rate_limited(phone)  # 2
    is_rate_limited(phone)  # 3
    assert is_rate_limited(phone) is True  # 4 — blocked


def test_seconds_until_reset_returns_positive_when_limited():
    phone = "test_reset_004"
    _clear(phone)
    is_rate_limited(phone)
    is_rate_limited(phone)
    is_rate_limited(phone)
    is_rate_limited(phone)  # trigger limit
    wait = seconds_until_reset(phone)
    assert 0 < wait <= 60


def test_seconds_until_reset_returns_zero_when_not_limited():
    phone = "test_reset_zero_005"
    _clear(phone)
    assert seconds_until_reset(phone) == 0


def test_different_phones_are_independent():
    phone_a = "test_indep_a_006"
    phone_b = "test_indep_b_007"
    _clear(phone_a)
    _clear(phone_b)
    # Exhaust phone_a
    is_rate_limited(phone_a)
    is_rate_limited(phone_a)
    is_rate_limited(phone_a)
    assert is_rate_limited(phone_a) is True
    # phone_b should still be free
    assert is_rate_limited(phone_b) is False


def test_old_requests_expire_from_window():
    """Simulate a request that happened more than 60 seconds ago."""
    phone = "test_expire_008"
    _clear(phone)
    # Inject timestamps outside the window manually
    past = time.time() - 65
    _request_log[phone] = [past, past, past]
    # Should not be limited since those are expired
    assert is_rate_limited(phone) is False
