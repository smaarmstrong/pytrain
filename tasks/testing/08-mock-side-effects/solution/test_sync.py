import pytest
from unittest.mock import create_autospec, patch

import sync


def fetch_mock(side_effect):
    return create_autospec(sync.fetch, side_effect=side_effect)


def test_success_on_first_try_calls_fetch_once_with_url_only():
    m = fetch_mock(["payload"])
    with patch("sync.fetch", m):
        assert sync.fetch_with_retry("http://x") == "payload"
    m.assert_called_once_with("http://x")


def test_retries_connection_errors_then_succeeds():
    m = fetch_mock([ConnectionError("down"), ConnectionError("down"), "payload"])
    with patch("sync.fetch", m):
        assert sync.fetch_with_retry("http://x") == "payload"
    assert m.call_count == 3


def test_reraises_after_attempts_exhausted():
    m = fetch_mock([ConnectionError("down"), ConnectionError("still down")])
    with patch("sync.fetch", m):
        with pytest.raises(ConnectionError, match="still down"):
            sync.fetch_with_retry("http://x", attempts=2)
    assert m.call_count == 2


def test_other_exceptions_propagate_immediately():
    m = fetch_mock([ValueError("boom")])
    with patch("sync.fetch", m):
        with pytest.raises(ValueError, match="boom"):
            sync.fetch_with_retry("http://x")
    m.assert_called_once_with("http://x")
