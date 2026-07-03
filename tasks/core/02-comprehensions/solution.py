def squares_of_evens(nums) -> list:
    return [n * n for n in nums if n % 2 == 0]


def word_lengths(words) -> dict:
    return {w.lower(): len(w) for w in words if w}


def distinct_initials(names) -> set:
    return {name[0].upper() for name in names if name}


def flatten_matrix(matrix) -> list:
    return [x for row in matrix for x in row]


def parity_labels(nums) -> list:
    return ["even" if n % 2 == 0 else "odd" for n in nums]
