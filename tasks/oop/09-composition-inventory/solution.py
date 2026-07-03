class Inventory:
    def __init__(self, items=None):
        self._items = list(items) if items is not None else []
        self.history = []

    def add(self, item):
        self._items.append(item)
        self.history.append(("add", item))

    def remove(self, item):
        self._items.remove(item)  # ValueError propagates before recording
        self.history.append(("remove", item))

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._items

    def __getitem__(self, index):
        return self._items[index]

    def __iter__(self):
        return iter(self._items)
