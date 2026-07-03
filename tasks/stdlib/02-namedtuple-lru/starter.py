Track = None  # TODO: build with collections.namedtuple("Track", ...)


class LRUCache:
    def __init__(self, capacity):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def put(self, key, value):
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __contains__(self, key):
        raise NotImplementedError
