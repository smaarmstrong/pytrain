def max_window_sum(nums, k):
    if k <= 0:
        raise ValueError("k must be positive")
    if k > len(nums):
        return None
    current = sum(nums[:k])
    best = current
    for j in range(k, len(nums)):
        current += nums[j] - nums[j - k]
        best = max(best, current)
    return best


def longest_unique_substring(s):
    last_seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


def pair_with_sum_sorted(nums, target):
    i, j = 0, len(nums) - 1
    while i < j:
        total = nums[i] + nums[j]
        if total == target:
            return (i, j)
        if total < target:
            i += 1
        else:
            j -= 1
    return None
