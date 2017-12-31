#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
There are two sorted arrays nums1 and nums2 of size m and n respectively.

Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).

Example 1:
nums1 = [1, 3]
nums2 = [2]

The median is 2.0
Example 2:
nums1 = [1, 2]
nums2 = [3, 4]

The median is (2 + 3)/2 = 2.5

SOLUTION:
    Lets say we have array a and array b with m and n elements respectively
    The idea is for each step, we remove an equal amount of elements from both
    arrays
    Which amount? Half the amount of the smaller array
    Which half? Lets call l the half elements of the smaller array
    If the median of a is smaller than that of b we remove l elements from the left of a
    and l elements from the right of b, not taken into account the medians themselves.
    Which means for odd elements we take (total-1) / 2, for even we remove total/2 - 1
    Untill one or both array has only one element. They are the medians that we search for.
"""

def midx(idx):
    return sum(idx) / 2

def whole_median(nums, idx):
    return nums[midx(idx)]

def length(idx):
    return idx[1] - idx[0]


def brute_median_of_2(nums1, nums2):
    s = sorted(nums1 + nums2)
    return median(s)

def median(nums):
    if len(nums) == 1:
        return nums[0]
    if len(nums) % 2 == 1:
        return nums[len(nums) / 2]
    else:
        m = len(nums) / 2
        return (nums[m-1] + nums[m]) / 2.0


def median_of_2(nums1, idx1, nums2, idx2):
    m, n = length(idx1), length(idx2)
    if m + n <= 10:
        # brute force to avoid tedious edge cases
        return brute_median_of_2(nums1[idx1[0]:idx1[1]], nums2[idx2[0]:idx2[1]])

    l = min(m, n)
    if l >= 4:
        # min(m,n)/2 - 1 to not removing the median in odd cases
        l = l/2 - (1 if l % 2 == 0 else 0)
    else:
        l = l / 2

    if l == 0:
        # one of them has only 1 number
        if n == 1:
            v = nums2[idx2[0]]
            nums = nums1
            idx = idx1
        else:
            v = nums1[idx1[0]]
            nums = nums2
            idx = idx2

        med = whole_median(nums, idx)
        mid = midx(idx)
        if (m + n) % 2 == 1:
            if v >= med:
                return med
            elif v >= nums[mid-1]:
                return v
            else:
                return nums[mid-1]
        else:
            if nums[mid-1] <= v <= nums[mid+1]:
                return (med + v) / 2.0
            elif v >= med:
                return (med + nums[mid+1]) / 2.0
            else:
                return (med + nums[mid-1]) / 2.0
    else:
        if whole_median(nums1, idx1) <= whole_median(nums2, idx2):
            idx1 = (idx1[0] + l, idx1[1])
            idx2 = (idx2[0], idx2[1] - l)
        else:
            idx1 = (idx1[0], idx1[1] - l)
            idx2 = (idx2[0] + l, idx2[1])

        return median_of_2(nums1, idx1, nums2, idx2)

class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """

        if not nums1:
            return median(nums2)
        elif not nums2:
            return median(nums1)

        return median_of_2(nums1, (0, len(nums1)), nums2, (0, len(nums2)))

import sys
from utils.templates import fail_string
import random

def sample_nums(n):
    return sorted(random.sample(range(n*10), n))

def test():
    solution = Solution()
    for case, ans in [
        ([[1, 2, 5, 6], [3, 4]], 3.5),
        ([[472, 490, 503, 515, 532, 539, 544, 548, 549, 555], [482, 500, 510, 531, 537, 538, 550, 565, 579, 590]], -1),
        ([[20, 34, 36, 37, 40, 42, 52, 61, 90, 98, 99, 109, 156, 165, 173, 174, 196, 199, 213, 238, 247, 279, 286, 292, 306, 309, 313, 321, 322, 331, 337, 342, 346, 357, 365, 385, 403, 414, 444, 446, 447, 454, 461, 464, 467, 472, 490, 503, 515, 532, 539, 544, 548, 549, 555, 567, 577, 591, 594, 599, 609, 624, 629, 641, 661, 663, 670, 672, 674, 711, 716, 725, 783, 786, 789, 804, 807, 823, 831, 840, 842, 850, 857, 859, 865, 872, 873, 898, 906, 943, 947, 953, 954, 964, 971, 972, 987, 989, 990, 993], [25, 45, 51, 58, 59, 60, 65, 75, 82, 102, 105, 133, 166, 171, 179, 183, 209, 237, 240, 241, 244, 250, 251, 267, 289, 290, 299, 316, 325, 353, 363, 373, 376, 384, 387, 404, 407, 409, 414, 416, 421, 448, 455, 459, 465, 482, 500, 510, 531, 537, 538, 550, 565, 579, 590, 591, 599, 608, 615, 623, 636, 637, 638, 644, 661, 662, 667, 675, 677, 687, 700, 704, 731, 745, 787, 799, 802, 818, 837, 845, 862, 875, 877, 883, 899, 905, 912, 922, 923, 928, 931, 947, 954, 956, 959, 964, 979, 992, 998, 999]], -1),
        ([sample_nums(10000), sample_nums(10000)], -1),
        ([sample_nums(10), sample_nums(3)], -1),
        # ([sample_nums(10000), sample_nums(1)], -1),
        ([[1, 3], [2]], 2),
        ([[1, 2], [3, 4]], 2.5),
        ([[4,6,8,10,12], [9]], 8.5),
        ([[4,6,8,10,12], [13]], 9),
        ([[4,6,8,10,12], [5,7,9,11,13]], 8.5),
        ([[4,6,8], [5,7,9]], 6.5),
        ([[4,6,8,10], [5,7,9]], 7),
    ]:
        res = solution.findMedianSortedArrays(*case)
        try:
            if ans == -1:
                ans = brute_median_of_2(*case)

            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    for i in range(100):
        test()