class Shelf:
    def __init__(self, titles):
        self._titles = list(titles)

    def __len__(self):
        return len(self._titles)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return Shelf(self._titles[index])
        return self._titles[index]

    def __contains__(self, title):
        return title in self._titles

    def __iter__(self):
        return iter(self._titles)
