def find_value(nums: list[int] | range, value: int) -> bool:
    """
    Find value in sorted sequence
    :param nums: sequence of integers. Could be empty
    :param value: integer to find
    :return: True if value exists, False otherwise
    """
    left = 0
    right = len(nums) - 1
    while left <= right:
        median = (left + right) // 2
        if nums[median] < value:
            left = median + 1
        elif nums[median] > value:
            right = median - 1
        else:
            return True

    return False
