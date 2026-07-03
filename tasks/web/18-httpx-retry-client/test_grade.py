import httpx
import pytest

from pytrain_grader import load_solution, get_attr


@pytest.fixture()
def APIClient():
    mod = load_solution()
    return get_attr(mod, "APIClient")


def make(APIClient, handler, **kwargs):
    return APIClient("https://api.test", transport=httpx.MockTransport(handler), **kwargs)


def test_success_first_try_returns_parsed_json(APIClient):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(200, json={"items": [1, 2, 3]})

    api = make(APIClient, handler)
    assert api.get_json("/things") == {"items": [1, 2, 3]}
    assert len(calls) == 1  # no pointless retries on success
    api.close()


def test_path_is_joined_onto_base_url(APIClient):
    seen = []

    def handler(request):
        seen.append((request.url.host, request.url.path, request.method))
        return httpx.Response(200, json={})

    api = make(APIClient, handler)
    api.get_json("/widgets/7")
    assert seen == [("api.test", "/widgets/7", "GET")]
    api.close()


def test_5xx_is_retried_until_success(APIClient):
    calls = []

    def handler(request):
        calls.append(1)
        if len(calls) < 3:
            return httpx.Response(500)
        return httpx.Response(200, json={"ok": True})

    api = make(APIClient, handler)  # default max_retries=3 allows 4 attempts
    assert api.get_json("/flaky") == {"ok": True}
    assert len(calls) == 3
    api.close()


def test_5xx_exhausted_raises_http_status_error(APIClient):
    calls = []

    def handler(request):
        calls.append(1)
        return httpx.Response(503)

    api = make(APIClient, handler, max_retries=2)
    with pytest.raises(httpx.HTTPStatusError):
        api.get_json("/down")
    assert len(calls) == 3  # max_retries + 1 attempts, no more
    api.close()


def test_4xx_raises_immediately_without_retry(APIClient):
    calls = []

    def handler(request):
        calls.append(1)
        return httpx.Response(404)

    api = make(APIClient, handler, max_retries=3)
    with pytest.raises(httpx.HTTPStatusError) as excinfo:
        api.get_json("/missing")
    assert excinfo.value.response.status_code == 404
    assert len(calls) == 1
    api.close()


def test_transport_errors_are_retried(APIClient):
    calls = []

    def handler(request):
        calls.append(1)
        if len(calls) < 3:
            raise httpx.ConnectTimeout("boom")
        return httpx.Response(200, json={"recovered": True})

    api = make(APIClient, handler)
    assert api.get_json("/slow") == {"recovered": True}
    assert len(calls) == 3
    api.close()


def test_transport_errors_exhausted_reraise(APIClient):
    calls = []

    def handler(request):
        calls.append(1)
        raise httpx.ConnectError("no route")

    api = make(APIClient, handler, max_retries=1)
    with pytest.raises(httpx.TransportError):
        api.get_json("/unreachable")
    assert len(calls) == 2
    api.close()


def test_max_retries_zero_means_single_attempt(APIClient):
    calls = []

    def handler(request):
        calls.append(1)
        return httpx.Response(500)

    api = make(APIClient, handler, max_retries=0)
    with pytest.raises(httpx.HTTPStatusError):
        api.get_json("/once")
    assert len(calls) == 1
    api.close()


def test_timeout_is_configured_on_requests(APIClient):
    seen = []

    def handler(request):
        seen.append(request.extensions.get("timeout", {}))
        return httpx.Response(200, json={})

    api = make(APIClient, handler, timeout=3.5)
    api.get_json("/t")
    assert seen and seen[0].get("read") == 3.5
    api.close()


def test_zero_backoff_is_fast(APIClient):
    # backoff defaults to 0.0: exhausting several retries must not sleep.
    import time

    def handler(request):
        return httpx.Response(500)

    api = make(APIClient, handler, max_retries=5)
    t0 = time.monotonic()
    with pytest.raises(httpx.HTTPStatusError):
        api.get_json("/d")
    assert time.monotonic() - t0 < 2.0  # generous; a real backoff would exceed this
    api.close()
