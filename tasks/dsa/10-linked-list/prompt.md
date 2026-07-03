# Singly linked list: build, reverse, cycle

A singly linked list is a chain of node objects, each with two attributes:

- `value` — the payload
- `next` — the next node, or `None` at the end of the chain

The starter gives you a `Node` class. IMPORTANT: the grader passes in its
*own* node objects that have the same `value`/`next` attributes (they are not
instances of your `Node`), so rely only on those two attributes — never on
`isinstance` checks.

In `solution.py`, implement:

```python
def build_linked(values):
    """Build a fresh chain of nodes from a Python list.

    Return the head node, or None for []. The chain's values, in order,
    are exactly `values` (duplicates and None payloads included), and the
    last node's `next` is None.
    """

def to_list(head):
    """Collect the values of a cycle-free chain into a Python list.

    to_list(None) == []. Inverse of build_linked.
    """

def reverse_linked(head):
    """Reverse the chain and return the new head.

    reverse_linked(None) is None. You may relink the existing nodes in
    place (the classic three-pointer walk) or build new nodes — the grader
    only inspects the returned head.
    """

def has_cycle(head):
    """True if following .next from head ever revisits a node.

    has_cycle(None) is False. The cycle may loop back to any node,
    including head itself (a one-node self-loop is a cycle). Node VALUES
    may repeat in a perfectly straight list — detect revisited NODES, not
    repeated values. Floyd's tortoise-and-hare or an `id()` set both work.
    """
```

Examples:

```python
>>> head = build_linked([1, 2, 3])
>>> head.value, head.next.value, head.next.next.next
(1, 2, None)
>>> to_list(build_linked([1, 2, 3]))
[1, 2, 3]
>>> to_list(reverse_linked(build_linked([1, 2, 3])))
[3, 2, 1]
>>> has_cycle(build_linked([7, 7, 7]))
False
```
