import multiprocessing  # noqa: F401
import pickle           # noqa: F401


def pool_map(fn, items, processes=4):
    """multiprocessing.Pool map, results in input order."""
    raise NotImplementedError


def is_picklable(obj):
    """True iff pickle.dumps(obj) succeeds."""
    raise NotImplementedError


def split_picklable(objs):
    """-> (picklable_objs, unpicklable_objs), order preserved."""
    raise NotImplementedError
