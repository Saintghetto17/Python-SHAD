from collections.abc import Sequence


def find_median(nums1: Sequence[int], nums2: Sequence[int]) -> float:
    """
    Find median of two sorted sequences. At least one of sequences should be not empty.
    :param nums1: sorted sequence of integers
    :param nums2: sorted sequence of integers
    :return: middle value if sum of sequences' lengths is odd
             average of two middle values if sum of sequences' lengths is even
    """
    len1 = len(nums1)
    len2 = len(nums2)

    if (len1 > len2):
        return find_median(nums2, nums1)
    sum = len1 + len2
    counter = (len1 + len2 + 1) // 2
    left_ptr_1 = 0
    right_ptr_1 = len1
    while left_ptr_1 <= right_ptr_1:
        median_1 = (left_ptr_1 + right_ptr_1) // 2
        # obviously right side we don t need
        median_2 = counter - median_1

        left_value_1 = 0.0
        right_value_1 = 0.0
        left_value_2 = 0.0
        right_value_2 = 0.0
        if median_1 == 0:
            left_value_1 = float('-inf')
        else:
            left_value_1 = nums1[median_1 - 1]
        if median_1 == len1:
            right_value_1 = float('inf')
        else:
            right_value_1 = nums1[median_1]
        if median_2 == 0:
            left_value_2 = float('-inf')
        else:
            left_value_2 = nums2[median_2 - 1]
        if median_2 == len2:
            right_value_2 = float('inf')
        else:
            right_value_2 = nums2[median_2]
        if left_value_1 <= right_value_2 and left_value_2 <= right_value_1:
            if sum % 2 == 1:
                return float(max(left_value_1, left_value_2))
            else:
                return float((max(left_value_1, left_value_2) + min(right_value_1, right_value_2)) / 2.0)
        elif left_value_1 > right_value_2:
            right_ptr_1 = median_1 - 1
        else:
            left_ptr_1 = median_1 + 1
    assert False, "Not reachable"
