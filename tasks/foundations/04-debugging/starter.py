# Two functions that run fine but answer wrong. No traceback will save
# you — look inside the loop (prints or breakpoint()) and fix each bug.


def running_total(nums):
    """running_total([1, 2, 3]) -> [1, 3, 6] — the sum so far, per element."""
    totals = []
    total = 0
    for n in nums:
        total = n
        totals.append(total)
    return totals


def count_vowels(word):
    """count_vowels("debug") -> 2 — count of a/e/i/o/u (lowercase input)."""
    count = 0
    for ch in word:
        if ch not in "aeiou":
            count += 1
    return count


if __name__ == "__main__":
    print(running_total([1, 2, 3]), "<- want [1, 3, 6]")
    print(count_vowels("debug"), "<- want 2")
