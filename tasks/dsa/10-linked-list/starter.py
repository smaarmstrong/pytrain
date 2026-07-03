class Node:
    """A singly linked list node.

    The grader may pass its own objects exposing the same `value`/`next`
    attributes, so rely only on those — no isinstance checks.
    """

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def build_linked(values):
    """Build a chain of Nodes from a list; return the head (None for [])."""
    raise NotImplementedError


def to_list(head):
    """Collect the values of a cycle-free chain into a list."""
    raise NotImplementedError


def reverse_linked(head):
    """Reverse the chain; return the new head."""
    raise NotImplementedError


def has_cycle(head):
    """True if following .next from head ever revisits a node."""
    raise NotImplementedError
