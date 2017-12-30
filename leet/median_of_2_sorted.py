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
"""

import sys
from utils.templates import fail_string

def mid(idx):
    return sum(idx) / 2

def median(nums, idx):
    return nums[mid(idx)]

def recurse(nums1, idx1, nums2, idx2, counts):
    def is_single(idx):
        return idx[1] - idx[0] == 1

    def is_empty(idx):
        return idx[0] >= idx[1]

    def odd(idx):
        return not even(idx)

    def even(idx):
        return (idx[1] - idx[0]) % 2 == 0

    def first_half(idx):
        # first half range
        return idx[0], mid(idx)

    def second_half(idx):
        # second half range
        return mid(idx), idx[1]

    def length(idx):
        return idx[1] - idx[0]

    print 'Recursing on', nums1[idx1[0]:idx1[1]], nums2[idx2[0]:idx2[1]]
    # print 'Median 1', median(nums1, idx1)
    # print 'Median 2', median(nums2, idx2)

    lc, rc = counts
    print '\tCounts', counts
    if is_single(idx1) and is_single(idx2):
        return nums1[idx1[1]-1], nums2[idx2[1]-1]
    elif is_empty(idx1):
        # delta = RC - LC, idx2[0] - delta
        m = mid(idx2)
        if odd(idx2):
            return nums2[m], nums2[m]
        else:
            return nums2[m-1], nums2[m]
    elif is_empty(idx2):
        m = mid(idx1)
        if odd(idx1):
            return nums1[m], nums1[m]
        else:
            return nums1[m-1], nums1[m]

    if median(nums1, idx1) <= median(nums2, idx2):
        counts = (length(first_half(idx1)) + lc, length(second_half(idx2)) + rc)
        return recurse(nums2, first_half(idx2), nums1, second_half(idx1), counts)
    else:
        counts = (length(first_half(idx2)) + lc, length(second_half(idx1)) + rc)
        return recurse(nums1, first_half(idx1), nums2, second_half(idx2), counts)

def median_of_2(nums1, nums2):
    m = len(nums1)
    n = len(nums2)
    x, y = recurse(nums1, (0, m), nums2, (0, n), (0, 0))

    print 'median_indices', x, y

    if (m + n) % 2 == 0:
        return (x + y) / 2.0
    else:
        return max(x, y)

class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        return median_of_2(nums1, nums2)

def test():
    for case, ans in [
        ([[1, 3], [2]], 2),
        ([[1, 2], [3, 4]], 2.5),
        ([[4,6,8,10,12], [9]], 8.5),
        ([[4,6,8,10,12], [13]], 9),
        ([[4,6,8,10,12], [5,7,9,11,13]], 8.5),
        ([[4,6,8], [5,7,9]], 6.5),
        ([[4,6,8,10], [5,7,9]], 7),
    ]:
        res = median_of_2(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()