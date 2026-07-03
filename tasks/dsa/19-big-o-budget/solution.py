def max_subarray_sum(nums):
    """Kadane: best sum of a run ending here, carried left to right."""
    best = cur = nums[0]
    for x in nums[1:]:
        cur = x if cur < 0 else cur + x
        if cur > best:
            best = cur
    return best


def range_sums(nums, queries):
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    return [prefix[hi] - prefix[lo] for lo, hi in queries]
