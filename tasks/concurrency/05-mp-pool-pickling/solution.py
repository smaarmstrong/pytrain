import multiprocessing
import pickle


def pool_map(fn, items, processes=4):
    with multiprocessing.Pool(processes) as pool:
        return pool.map(fn, items)


def is_picklable(obj):
    try:
        pickle.dumps(obj)
        return True
    except Exception:  # noqa: BLE001 — pickling can raise many things
        return False


def split_picklable(objs):
    good, bad = [], []
    for obj in objs:
        (good if is_picklable(obj) else bad).append(obj)
    return good, bad
