# Stack & queue from scratch

In `solution.py`, implement two classes from first principles:

```python
class Stack:
    """LIFO: the most recently pushed item comes out first."""
    def push(self, item): ...
    def pop(self): ...        # remove & return the newest item; IndexError if empty
    def peek(self): ...       # return (don't remove) the newest item; IndexError if empty
    def is_empty(self): ...   # -> bool
    def __len__(self): ...    # number of items currently held

class Queue:
    """FIFO: the oldest enqueued item comes out first."""
    def enqueue(self, item): ...
    def dequeue(self): ...    # remove & return the oldest item; IndexError if empty
    def peek(self): ...       # return (don't remove) the oldest item; IndexError if empty
    def is_empty(self): ...   # -> bool
    def __len__(self): ...
```

Requirements:

- `pop`, `dequeue` and both `peek`s raise `IndexError` when the container is
  empty (any message).
- Items may be anything, including duplicates and `None` — `None` is a valid
  stored value, not a sentinel.
- A plain `list` backs a stack naturally; for the queue prefer
  `collections.deque` so both ends are cheap (no timing is enforced, but
  that's the idiomatic tool).

Examples:

```python
>>> s = Stack(); s.push(1); s.push(2); s.pop()
2
>>> q = Queue(); q.enqueue(1); q.enqueue(2); q.dequeue()
1
>>> len(q), q.is_empty()
(1, False)
```
