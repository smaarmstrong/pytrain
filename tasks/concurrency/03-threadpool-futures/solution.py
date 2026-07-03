from concurrent.futures import ThreadPoolExecutor, as_completed


def parallel_map(fn, items, max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(fn, items))


def try_map(fn, items, max_workers):
    out = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(fn, item): item for item in items}
        for fut in as_completed(futures):
            item = futures[fut]
            try:
                out[item] = ("ok", fut.result())
            except Exception as exc:  # noqa: BLE001
                out[item] = ("error", type(exc).__name__)
    return out


def first_result(fn, items, max_workers):
    # No `with` block: exiting the context manager would wait for ALL
    # futures; we want to return as soon as the first one lands.
    pool = ThreadPoolExecutor(max_workers=max_workers)
    try:
        futures = [pool.submit(fn, item) for item in items]
        for fut in as_completed(futures):
            return fut.result()
        raise ValueError("no items")
    finally:
        pool.shutdown(wait=False, cancel_futures=True)
