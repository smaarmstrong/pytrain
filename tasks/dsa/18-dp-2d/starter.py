def grid_paths(rows, cols, blocked=()):
    """Right/down paths through a grid avoiding blocked cells."""
    raise NotImplementedError


def edit_distance(a, b):
    """Levenshtein distance (insert/delete/substitute, cost 1 each)."""
    raise NotImplementedError


def lcs_length(a, b):
    """Length of the longest common subsequence."""
    raise NotImplementedError
