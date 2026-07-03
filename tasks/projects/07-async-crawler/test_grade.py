"""Grades the crawler entirely through httpx.MockTransport — no network,
no sockets. The grader builds the AsyncClient and hands it to the learner's
coroutines; every request is counted so retries/dedupe are observable.
"""
import asyncio
from collections import Counter

import httpx

from pytrain_grader import load_solution, get_attr


def get_fetch():
    mod = load_solution(filename="fetch.py", module_name="crawler_fetch")
    return get_attr(mod, "fetch_with_retry")


def get_crawl():
    mod = load_solution(filename="crawler.py", module_name="crawler_main")
    return get_attr(mod, "crawl")


class MockSite:
    """In-process site: pages dict, per-URL call counter, optional 503 runs.

    flaky[url] = N -> first N requests answer 503, then the real page.
    Pages whose value is an int are plain status responses (404, 500, ...).
    """

    def __init__(self, pages, flaky=None):
        self.pages = pages
        self.flaky = dict(flaky or {})
        self.calls = Counter()
        self.inflight = 0
        self.max_inflight = 0
        self.delay = 0.0

    async def handler(self, request):
        url = str(request.url)
        self.calls[url] += 1
        self.inflight += 1
        self.max_inflight = max(self.max_inflight, self.inflight)
        try:
            if self.delay:
                await asyncio.sleep(self.delay)
            if self.flaky.get(url, 0) >= self.calls[url]:
                return httpx.Response(503, json={"error": "try later"})
            page = self.pages.get(url)
            if page is None:
                return httpx.Response(404, json={"error": "not found"})
            if isinstance(page, int):
                return httpx.Response(page, json={"error": "boom"})
            return httpx.Response(200, json=page)
        finally:
            self.inflight -= 1

    def run(self, coro_fn):
        async def go():
            async with httpx.AsyncClient(
                    transport=httpx.MockTransport(self.handler)) as client:
                return await coro_fn(client)
        return asyncio.run(go())


ROOT = "https://site.test/"


def u(path):
    return ROOT.rstrip("/") + "/" + path


# -- fetch.py: fetch_with_retry ----------------------------------------------

def test_fetch_200_first_try_is_one_call():
    site = MockSite({ROOT: {"title": "Home"}})
    resp = site.run(lambda c: get_fetch()(c, ROOT))
    assert resp.status_code == 200
    assert resp.json()["title"] == "Home"
    assert site.calls[ROOT] == 1


def test_fetch_404_returns_immediately_without_retry():
    site = MockSite({})
    resp = site.run(lambda c: get_fetch()(c, u("nope")))
    assert resp.status_code == 404
    assert site.calls[u("nope")] == 1


def test_fetch_retries_through_503_then_succeeds():
    site = MockSite({ROOT: {"title": "Home"}}, flaky={ROOT: 2})
    resp = site.run(lambda c: get_fetch()(c, ROOT))
    assert resp.status_code == 200
    assert site.calls[ROOT] == 3


def test_fetch_gives_up_after_attempts_and_returns_last_503():
    site = MockSite({ROOT: {"title": "Home"}}, flaky={ROOT: 99})
    resp = site.run(lambda c: get_fetch()(c, ROOT))
    assert resp.status_code == 503
    assert site.calls[ROOT] == 3        # default attempts=3, total

    site = MockSite({ROOT: {"title": "Home"}}, flaky={ROOT: 99})
    resp = site.run(lambda c: get_fetch()(c, ROOT, 1))
    assert resp.status_code == 503
    assert site.calls[ROOT] == 1        # attempts is respected


# -- crawler.py: crawl --------------------------------------------------------

def basic_pages():
    return {
        ROOT: {"title": "Home", "links": [u("a"), u("b")]},
        u("a"): {"title": "A", "links": [u("b"), u("c")]},
        u("b"): {"title": "B", "links": [u("a")]},     # cycle + duplicate
        u("c"): {"title": "C"},                        # no "links" key at all
    }


def test_crawl_collects_all_titles():
    site = MockSite(basic_pages())
    result = site.run(lambda c: get_crawl()(ROOT, c))
    assert result == {ROOT: "Home", u("a"): "A", u("b"): "B", u("c"): "C"}


def test_crawl_fetches_each_url_exactly_once():
    site = MockSite(basic_pages())
    site.run(lambda c: get_crawl()(ROOT, c))
    assert site.calls == Counter({ROOT: 1, u("a"): 1, u("b"): 1, u("c"): 1})


def test_max_pages_caps_distinct_fetches():
    pages = {ROOT: {"title": "Home",
                    "links": [u(f"p{i}") for i in range(6)]}}
    for i in range(6):
        pages[u(f"p{i}")] = {"title": f"P{i}"}
    site = MockSite(pages)
    result = site.run(lambda c: get_crawl()(ROOT, c, 3))
    assert len(site.calls) == 3          # distinct URLs fetched
    assert sum(site.calls.values()) == 3  # and no re-fetches either
    assert result[ROOT] == "Home"
    assert len(result) == 3


def test_non_200_page_is_excluded_and_its_links_not_followed():
    pages = {
        ROOT: {"title": "Home", "links": [u("bad"), u("a")]},
        u("bad"): 500,
        u("a"): {"title": "A"},
    }
    site = MockSite(pages)
    result = site.run(lambda c: get_crawl()(ROOT, c))
    assert result == {ROOT: "Home", u("a"): "A"}
    assert site.calls[u("bad")] == 1


def test_404_link_is_fetched_once_but_excluded():
    pages = {ROOT: {"title": "Home", "links": [u("ghost"), u("a")]},
             u("a"): {"title": "A"}}
    site = MockSite(pages)
    result = site.run(lambda c: get_crawl()(ROOT, c))
    assert u("ghost") not in result
    assert site.calls[u("ghost")] == 1
    assert result == {ROOT: "Home", u("a"): "A"}


def test_crawl_retries_503_pages_and_drops_dead_ones():
    pages = {
        ROOT: {"title": "Home", "links": [u("flaky"), u("dead")]},
        u("flaky"): {"title": "Flaky"},
        u("dead"): {"title": "Never"},
    }
    site = MockSite(pages, flaky={u("flaky"): 2, u("dead"): 99})
    result = site.run(lambda c: get_crawl()(ROOT, c))
    assert result == {ROOT: "Home", u("flaky"): "Flaky"}
    assert site.calls[u("flaky")] == 3
    assert site.calls[u("dead")] == 3


def wide_pages(n):
    pages = {ROOT: {"title": "Home", "links": [u(f"w{i}") for i in range(n)]}}
    for i in range(n):
        pages[u(f"w{i}")] = {"title": f"W{i}"}
    return pages


def test_concurrency_limit_is_never_exceeded():
    site = MockSite(wide_pages(8))
    site.delay = 0.02
    result = site.run(lambda c: get_crawl()(ROOT, c, 20, 2))
    assert len(result) == 9
    assert site.max_inflight <= 2


def test_independent_pages_are_fetched_concurrently():
    site = MockSite(wide_pages(4))
    site.delay = 0.15   # generous overlap window: serial code shows inflight=1
    site.run(lambda c: get_crawl()(ROOT, c, 20, 3))
    assert site.max_inflight >= 2, (
        "sibling pages were fetched strictly one-by-one — crawl must issue "
        "up to `concurrency` requests in parallel"
    )
    assert site.max_inflight <= 3
