from collections import Counter
from itertools import accumulate, combinations, permutations, product


def dice_sums(n_dice, sides):
    return dict(Counter(sum(roll) for roll in product(range(1, sides + 1), repeat=n_dice)))


def unique_anagrams(word):
    return sorted({"".join(p) for p in permutations(word)})


def choose(items, k):
    return list(combinations(items, k))


def running(values, op):
    return list(accumulate(values, op))
