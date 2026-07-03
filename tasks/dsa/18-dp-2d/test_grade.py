import random
from functools import lru_cache

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return (get_attr(mod, "grid_paths"),
            get_attr(mod, "edit_distance"),
            get_attr(mod, "lcs_length"))


# --- trivially-correct oracles (small inputs only) ---------------------------

def oracle_grid(rows, cols, blocked):
    blocked = set(blocked)

    def walk(r, c):
        if (r, c) in blocked or r >= rows or c >= cols:
            return 0
        if (r, c) == (rows - 1, cols - 1):
            return 1
        return walk(r + 1, c) + walk(r, c + 1)

    return walk(0, 0)


def oracle_edit(a, b):
    @lru_cache(maxsize=None)
    def d(i, j):
        if i == 0:
            return j
        if j == 0:
            return i
        return min(d(i - 1, j) + 1,
                   d(i, j - 1) + 1,
                   d(i - 1, j - 1) + (a[i - 1] != b[j - 1]))

    return d(len(a), len(b))


def oracle_lcs(a, b):
    @lru_cache(maxsize=None)
    def l(i, j):
        if i == 0 or j == 0:
            return 0
        if a[i - 1] == b[j - 1]:
            return l(i - 1, j - 1) + 1
        return max(l(i - 1, j), l(i, j - 1))

    return l(len(a), len(b))


# --- grid_paths ----------------------------------------------------------------

def test_grid_basics():
    gp, _, _ = fns()
    assert gp(1, 1) == 1
    assert gp(2, 2) == 2
    assert gp(3, 3) == 6
    assert gp(1, 5) == 1
    assert gp(5, 1) == 1


def test_grid_blocked_cells():
    gp, _, _ = fns()
    assert gp(3, 3, blocked={(1, 1)}) == 2
    assert gp(3, 3, blocked={(0, 1), (1, 0)}) == 0   # walled in
    assert gp(2, 2, blocked={(0, 1)}) == 1
    assert gp(1, 1, blocked=set()) == 1


def test_grid_blocked_start_or_goal():
    gp, _, _ = fns()
    assert gp(3, 3, blocked={(0, 0)}) == 0
    assert gp(3, 3, blocked={(2, 2)}) == 0
    assert gp(1, 1, blocked={(0, 0)}) == 0


def test_grid_out_of_range_blocks_ignored():
    gp, _, _ = fns()
    assert gp(2, 2, blocked={(5, 5), (-1, 0), (0, 99)}) == 2


def test_grid_18x18_exact():
    gp, _, _ = fns()
    assert gp(18, 18) == 2333606220  # C(34, 17): recursion won't get here


def test_grid_80x80_with_wall_promptly():
    gp, _, _ = fns()
    # a wall across row 40 with one gap: every path funnels through
    # (39,13) -> (40,13) -> (41,13), so the count factorises exactly
    wall = {(40, c) for c in range(80) if c != 13}
    got = gp(80, 80, blocked=wall)
    top = gp(40, 14)      # (0,0) -> (39,13)
    bottom = gp(39, 67)   # (41,13) -> (79,79)
    assert got == top * bottom
    assert got > 0


def test_grid_randomized_vs_bruteforce():
    gp, _, _ = fns()
    rng = random.Random(42)
    for _ in range(60):
        rows, cols = rng.randrange(1, 7), rng.randrange(1, 7)
        blocked = {(rng.randrange(rows), rng.randrange(cols))
                   for _ in range(rng.randrange(0, 5))}
        assert gp(rows, cols, blocked=set(blocked)) == \
            oracle_grid(rows, cols, blocked), (rows, cols, blocked)


# --- edit_distance ----------------------------------------------------------------

def test_edit_classics():
    _, ed, _ = fns()
    assert ed("kitten", "sitting") == 3
    assert ed("flaw", "lawn") == 2
    assert ed("intention", "execution") == 5


def test_edit_edges():
    _, ed, _ = fns()
    assert ed("", "") == 0
    assert ed("", "abc") == 3
    assert ed("abc", "") == 3
    assert ed("same", "same") == 0
    assert ed("a", "b") == 1


def test_edit_is_symmetric():
    _, ed, _ = fns()
    assert ed("sunday", "saturday") == ed("saturday", "sunday") == 3


def test_edit_long_strings_promptly():
    _, ed, _ = fns()
    a = "ab" * 100          # 200 chars
    b = "ba" * 100
    assert ed(a, b) == 2    # rotate: delete leading 'a', append trailing 'a'
    assert ed("x" * 200, "x" * 150) == 50


def test_edit_randomized_vs_oracle():
    _, ed, _ = fns()
    rng = random.Random(42)
    for _ in range(80):
        a = "".join(rng.choice("abc") for _ in range(rng.randrange(0, 13)))
        b = "".join(rng.choice("abc") for _ in range(rng.randrange(0, 13)))
        assert ed(a, b) == oracle_edit(a, b), (a, b)


# --- lcs_length ---------------------------------------------------------------------

def test_lcs_classics():
    _, _, lcs = fns()
    assert lcs("abcde", "ace") == 3
    assert lcs("AGGTAB", "GXTXAYB") == 4
    assert lcs("abc", "xyz") == 0


def test_lcs_edges():
    _, _, lcs = fns()
    assert lcs("", "") == 0
    assert lcs("", "abc") == 0
    assert lcs("abc", "") == 0
    assert lcs("abc", "abc") == 3
    assert lcs("aaaa", "aa") == 2


def test_lcs_subsequence_not_substring():
    _, _, lcs = fns()
    assert lcs("axbxc", "abc") == 3  # scattered characters still count


def test_lcs_long_strings_promptly():
    _, _, lcs = fns()
    assert lcs("ab" * 100, "b" * 100) == 100
    assert lcs("x" * 200, "y" * 200) == 0


def test_lcs_randomized_vs_oracle():
    _, _, lcs = fns()
    rng = random.Random(42)
    for _ in range(80):
        a = "".join(rng.choice("ab") for _ in range(rng.randrange(0, 13)))
        b = "".join(rng.choice("ab") for _ in range(rng.randrange(0, 13)))
        assert lcs(a, b) == oracle_lcs(a, b), (a, b)
