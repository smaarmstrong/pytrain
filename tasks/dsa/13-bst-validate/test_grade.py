import random
from types import SimpleNamespace

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return (get_attr(mod, "bst_insert"),
            get_attr(mod, "inorder_values"),
            get_attr(mod, "is_valid_bst"))


def node(value, left=None, right=None):
    return SimpleNamespace(value=value, left=left, right=right)


def oracle_inorder(t):
    return [] if t is None else oracle_inorder(t.left) + [t.value] + oracle_inorder(t.right)


def oracle_valid(t, lo=None, hi=None):
    if t is None:
        return True
    if lo is not None and t.value <= lo:
        return False
    if hi is not None and t.value >= hi:
        return False
    return oracle_valid(t.left, lo, t.value) and oracle_valid(t.right, t.value, hi)


def grow(insert, values):
    root = None
    for v in values:
        root = insert(root, v)
    return root


# --- bst_insert ---------------------------------------------------------------

def test_insert_into_empty():
    ins, _, _ = fns()
    root = ins(None, 5)
    assert root is not None
    assert root.value == 5 and root.left is None and root.right is None


def test_insert_builds_a_search_tree():
    ins, _, _ = fns()
    root = grow(ins, [5, 3, 8, 1, 4])
    assert oracle_inorder(root) == [1, 3, 4, 5, 8]
    assert oracle_valid(root)


def test_insert_ignores_duplicates():
    ins, _, _ = fns()
    root = grow(ins, [5, 3, 8, 3, 5, 8, 8])
    assert oracle_inorder(root) == [3, 5, 8]
    assert oracle_valid(root)


def test_insert_sorted_input_makes_a_deep_valid_tree():
    ins, _, _ = fns()
    root = grow(ins, range(200))  # worst case: a 200-deep skewed chain
    assert oracle_inorder(root) == list(range(200))
    assert oracle_valid(root)


def test_insert_randomized_round_trip():
    ins, _, _ = fns()
    rng = random.Random(42)
    for _ in range(40):
        values = [rng.randrange(50) for _ in range(rng.randrange(0, 60))]
        root = grow(ins, values)
        assert oracle_inorder(root) == sorted(set(values)), values
        assert oracle_valid(root), values


# --- inorder_values -------------------------------------------------------------

def test_inorder_empty_and_single():
    _, ino, _ = fns()
    assert ino(None) == []
    assert ino(node(7)) == [7]


def test_inorder_on_grader_bst():
    _, ino, _ = fns()
    t = node(5, node(3, node(1), node(4)), node(8))
    assert ino(t) == [1, 3, 4, 5, 8]


def test_inorder_on_non_bst_is_plain_inorder():
    _, ino, _ = fns()
    # NOT a search tree — in-order must still be left, node, right.
    t = node(1, node(9, None, node(2)), node(0))
    assert ino(t) == [9, 2, 1, 0]


def test_inorder_randomized():
    _, ino, _ = fns()
    rng = random.Random(42)
    for _ in range(30):
        t = None
        for v in rng.sample(range(1000), rng.randrange(0, 40)):
            t = grader_bst_insert(t, v)
        assert ino(t) == oracle_inorder(t)


def grader_bst_insert(t, v):
    if t is None:
        return node(v)
    if v < t.value:
        t.left = grader_bst_insert(t.left, v)
    elif v > t.value:
        t.right = grader_bst_insert(t.right, v)
    return t


# --- is_valid_bst ---------------------------------------------------------------

def test_valid_empty_single_and_small():
    _, _, valid = fns()
    assert valid(None) is True
    assert valid(node(1)) is True
    assert valid(node(2, node(1), node(3))) is True


def test_invalid_immediate_child():
    _, _, valid = fns()
    assert valid(node(2, node(3), None)) is False   # left child too big
    assert valid(node(2, None, node(1))) is False   # right child too small


def test_invalid_grandchild_violates_grandparent():
    _, _, valid = fns()
    # 6 > 3 locally, but 6 sits inside 5's LEFT subtree -> invalid
    assert valid(node(5, node(3, node(1), node(6)), node(8))) is False
    # mirror case: values in 5's RIGHT subtree must all exceed 5
    assert valid(node(5, node(3), node(7, node(6), node(9)))) is True
    assert valid(node(5, node(3), node(7, node(2), node(9)))) is False


def test_duplicates_are_invalid():
    _, _, valid = fns()
    assert valid(node(2, node(2), None)) is False
    assert valid(node(2, None, node(2))) is False


def test_valid_randomized():
    _, _, valid = fns()
    rng = random.Random(42)
    for _ in range(60):
        t = None
        values = rng.sample(range(200), rng.randrange(1, 30))
        for v in values:
            t = grader_bst_insert(t, v)
        assert valid(t) is True, values
        # sabotage one node's value and expect (oracle-confirmed) invalidity
        nodes = []
        stack = [t]
        while stack:
            n = stack.pop()
            nodes.append(n)
            stack.extend(c for c in (n.left, n.right) if c is not None)
        victim = rng.choice(nodes)
        old = victim.value
        victim.value = rng.randrange(200)
        assert valid(t) is oracle_valid(t), (values, old, victim.value)
