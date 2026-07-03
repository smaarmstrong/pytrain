import random
from collections import deque
from types import SimpleNamespace

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return (get_attr(mod, "build_tree"),
            get_attr(mod, "preorder"),
            get_attr(mod, "inorder"),
            get_attr(mod, "postorder"),
            get_attr(mod, "level_order"))


# --- grader-owned tree helpers (only value/left/right attributes) -----------

def node(value, left=None, right=None):
    return SimpleNamespace(value=value, left=left, right=right)


def oracle_pre(t):
    return [] if t is None else [t.value] + oracle_pre(t.left) + oracle_pre(t.right)


def oracle_in(t):
    return [] if t is None else oracle_in(t.left) + [t.value] + oracle_in(t.right)


def oracle_post(t):
    return [] if t is None else oracle_post(t.left) + oracle_post(t.right) + [t.value]


def oracle_levels(t):
    if t is None:
        return []
    out, level = [], [t]
    while level:
        out.append([n.value for n in level])
        level = [c for n in level for c in (n.left, n.right) if c is not None]
    return out


def encode(t):
    """Compact level-order encoding — the exact format build_tree decodes."""
    if t is None:
        return []
    out, queue = [t.value], deque([t])
    while queue:
        n = queue.popleft()
        for c in (n.left, n.right):
            out.append(None if c is None else c.value)
            if c is not None:
                queue.append(c)
    while out and out[-1] is None:
        out.pop()
    return out


def random_tree(rng, n):
    """A random shape with n nodes, values 0..n-1 (distinct)."""
    if n == 0:
        return None
    root = node(0)
    nodes = [root]
    for v in range(1, n):
        parent = rng.choice(nodes)
        while (parent.left is not None) and (parent.right is not None):
            parent = rng.choice(nodes)
        child = node(v)
        if parent.left is None and (parent.right is not None or rng.random() < 0.5):
            parent.left = child
        else:
            parent.right = child
        nodes.append(child)
    return root


def sample_tree():
    # the prompt's [1, 2, 3, None, 4] tree
    return node(1, node(2, None, node(4)), node(3))


# --- build_tree --------------------------------------------------------------

def test_build_empty():
    bt, *_ = fns()
    assert bt([]) is None


def test_build_single():
    bt, *_ = fns()
    root = bt([9])
    assert root.value == 9 and root.left is None and root.right is None


def test_build_prompt_example():
    bt, *_ = fns()
    root = bt([1, 2, 3, None, 4])
    assert oracle_levels(root) == [[1], [2, 3], [4]]
    assert oracle_pre(root) == [1, 2, 4, 3]


def test_build_list_may_end_early():
    bt, *_ = fns()
    root = bt([1, 2, 3])  # no entries for 2's or 3's children
    assert oracle_levels(root) == [[1], [2, 3]]


def test_build_none_consumes_no_children():
    bt, *_ = fns()
    # None children must NOT eat the following values.
    root = bt([1, None, 2, 3, None])
    assert oracle_levels(root) == [[1], [2], [3]]
    assert oracle_in(root) == [1, 3, 2]


def test_build_randomized_round_trip():
    bt, *_ = fns()
    rng = random.Random(42)
    for _ in range(40):
        t = random_tree(rng, rng.randrange(0, 25))
        built = bt(encode(t))
        assert oracle_pre(built) == oracle_pre(t)
        assert oracle_in(built) == oracle_in(t)


# --- DFS traversals -----------------------------------------------------------

def test_traversals_empty_and_single():
    _, pre, ino, post, lev = fns()
    for f in (pre, ino, post):
        assert f(None) == []
        assert f(node(7)) == [7]
    assert lev(None) == []
    assert lev(node(7)) == [[7]]


def test_traversals_prompt_example():
    _, pre, ino, post, lev = fns()
    t = sample_tree()
    assert pre(t) == [1, 2, 4, 3]
    assert ino(t) == [2, 4, 1, 3]
    assert post(t) == [4, 2, 3, 1]
    assert lev(t) == [[1], [2, 3], [4]]


def test_traversals_duplicate_values():
    _, pre, ino, post, lev = fns()
    t = node(5, node(5), node(5, node(5), None))
    assert pre(t) == [5, 5, 5, 5]
    assert ino(t) == [5, 5, 5, 5]
    assert post(t) == [5, 5, 5, 5]
    assert lev(t) == [[5], [5, 5], [5]]


def test_skewed_tree_100_deep():
    _, pre, ino, post, lev = fns()
    t = None
    for v in range(100):
        t = node(v, t, None)  # left-skewed chain
    assert pre(t) == list(range(99, -1, -1))
    assert ino(t) == list(range(100))
    assert post(t) == list(range(100))
    assert lev(t) == [[v] for v in range(99, -1, -1)]


def test_traversals_randomized_vs_oracle():
    _, pre, ino, post, lev = fns()
    rng = random.Random(42)
    for _ in range(50):
        t = random_tree(rng, rng.randrange(0, 30))
        assert pre(t) == oracle_pre(t)
        assert ino(t) == oracle_in(t)
        assert post(t) == oracle_post(t)
        assert lev(t) == oracle_levels(t)
