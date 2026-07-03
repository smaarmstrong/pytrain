from concurrent.futures import ProcessPoolExecutor


def process_map(fn, items, max_workers=4):
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(fn, items))


def map_reduce(map_fn, reduce_fn, items, max_workers=4):
    return reduce_fn(process_map(map_fn, items, max_workers=max_workers))
