from collections import deque


class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)


class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def peek(self):
        if not self._items:
            raise IndexError("peek at empty queue")
        return self._items[0]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)
