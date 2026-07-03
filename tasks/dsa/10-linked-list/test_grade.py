import random
from types import SimpleNamespace

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return (get_attr(mod, "build_linked"),
            get_attr(mod, "to_list"),
            get_attr(mod, "reverse_linked"),
            get_attr(mod, "has_cycle"))


def chain(values):
    """A grader-owned chain of plain objects with value/next attributes."""
    head = None
    for v in reversed(values):
        head = SimpleNamespace(value=v, next=head)
    return head


def cyclic(values, entry):
    """A chain whose tail loops back to values[entry]'s node."""
    nodes = [SimpleNamespace(value=v, next=None) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    nodes[-1].next = nodes[entry]
    return nodes[0]


def walk(head, limit=10_000):
    """Traverse via .value/.next, guarding against accidental cycles."""
    out, node = [], head
    while node is not None:
        out.append(node.value)
        node = node.next
        assert len(out) <= limit, "walked >10k nodes — accidental cycle?"
    return out


# --- build_linked -----------------------------------------------------------

def test_build_empty_is_none():
    bl, _, _, _ = fns()
    assert bl([]) is None


def test_build_chains_values_in_order():
    bl, _, _, _ = fns()
    assert walk(bl([1, 2, 3])) == [1, 2, 3]
    assert walk(bl([7])) == [7]
    assert walk(bl([5, 5, 5])) == [5, 5, 5]           # duplicates kept
    assert walk(bl([None, 0, ""])) == [None, 0, ""]   # falsy payloads are values


def test_build_terminates_with_none():
    bl, _, _, _ = fns()
    head = bl([1, 2])
    assert head.value == 1
    assert head.next.value == 2
    assert head.next.next is None


# --- to_list ----------------------------------------------------------------

def test_to_list_on_grader_nodes():
    _, tl, _, _ = fns()
    assert tl(None) == []
    assert tl(chain([4])) == [4]
    assert tl(chain(["a", "b", "a"])) == ["a", "b", "a"]


def test_build_to_list_round_trip():
    bl, tl, _, _ = fns()
    for values in ([], [1], [1, 2, 3], [0, 0, None, 0]):
        assert tl(bl(list(values))) == values


# --- reverse_linked ---------------------------------------------------------

def test_reverse_basics():
    _, _, rv, _ = fns()
    assert rv(None) is None
    assert walk(rv(chain([9]))) == [9]
    assert walk(rv(chain([1, 2, 3]))) == [3, 2, 1]
    assert walk(rv(chain([2, 2, 5]))) == [5, 2, 2]


def test_reverse_ends_with_none():
    _, _, rv, _ = fns()
    head = rv(chain([1, 2]))
    assert head.value == 2 and head.next.value == 1 and head.next.next is None


def test_reverse_randomized():
    _, _, rv, _ = fns()
    rng = random.Random(42)
    for _ in range(60):
        values = [rng.randrange(10) for _ in range(rng.randrange(0, 40))]
        got = rv(chain(values))
        assert walk(got) == values[::-1]


# --- has_cycle ---------------------------------------------------------------

def test_no_cycle():
    _, _, _, hc = fns()
    assert hc(None) is False
    assert hc(chain([1])) is False
    assert hc(chain([1, 2, 3])) is False
    assert hc(chain([7, 7, 7, 7])) is False  # repeated VALUES are not a cycle


def test_cycles_detected():
    _, _, _, hc = fns()
    assert hc(cyclic([1], 0)) is True                # self-loop
    assert hc(cyclic([1, 2, 3, 4], 0)) is True        # tail -> head
    assert hc(cyclic([1, 2, 3, 4, 5], 2)) is True     # tail -> middle
    assert hc(cyclic([9, 9], 1)) is True              # tail self-loop


def test_cycle_randomized():
    _, _, _, hc = fns()
    rng = random.Random(42)
    for _ in range(60):
        n = rng.randrange(1, 30)
        values = [rng.randrange(5) for _ in range(n)]
        if rng.random() < 0.5:
            assert hc(cyclic(values, rng.randrange(n))) is True
        else:
            assert hc(chain(values)) is False
