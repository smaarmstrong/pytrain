def eager_squares(nums) -> list:
    return [n * n for n in nums]


def lazy_squares(nums):
    return (n * n for n in nums)
