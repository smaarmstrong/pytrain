def char_frequency(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    return counts


def two_sum(nums, target):
    seen = {}  # value -> index
    for j, x in enumerate(nums):
        i = seen.get(target - x)
        if i is not None:
            return (i, j)
        seen.setdefault(x, j)
    return None


def group_anagrams(words):
    groups = {}
    for w in words:
        groups.setdefault("".join(sorted(w)), []).append(w)
    return list(groups.values())
