#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given two arrays of length m and n with digits 0-9 representing two numbers. Create the maximum number of length k <= m + n from digits of the two. The relative order of the digits from the same array must be preserved. Return an array of the k digits. You should try to optimize your time and space complexity.

Example 1:
nums1 = [3, 4, 6, 5]
nums2 = [9, 1, 2, 5, 8, 3]
k = 5
return [9, 8, 6, 5, 3]

Example 2:
nums1 = [6, 7]
nums2 = [6, 0, 4]
k = 5
return [6, 7, 6, 0, 4]

Example 3:
nums1 = [3, 9]
nums2 = [8, 9]
k = 3
return [9, 8, 9]

SOLUTION:
    The idea is to brute-force k numbers from either array a or b. Sucessively check all scenarios where
    i numbers come from a (hence k-i from b). This takes O(k).
    For each scenario: i comes from a and k-i from b. We need to solve separate case efficently.
    Then the problem reduces to:
        - Select best numbers from a and b (k cases, i from a, k - i from b): O(m+n)
        - Merge them O(k2)
        - Select the largest among all merged numbers O(k2)
        Total: O((m+n)k + k3)

    To efficiently select largest possible number from a or b, stacks are required.
    It takes linear time to solve using stacks.

"""

DEBUG = False

def max_number_from_array(nums, k):
    if k < 1 or not nums or k > len(nums):
        return []

    stack = []
    for i, v in enumerate(nums):
        while stack and len(nums) - i + len(stack) > k and v > stack[-1]:
            stack.pop()
        if len(stack) < k:
            stack.append(v)

    return stack

def merge(a, b, i, j):
    res = []
    m, n = len(a), len(b)
    while i < m or j < n:
        if i == m:
            res += b[j:]
            break
        elif j == n:
            res += a[i:]
            break
        elif a[i] > b[j]:
            res.append(a[i])
            i += 1
        elif a[i] < b[j]:
            res.append(b[j])
            j += 1
        else:
            ii = i
            jj = j
            while ii < m and jj < n and a[ii] == b[jj]:
                ii += 1
                jj += 1

            take = 1
            if ii < m and jj < n:
                take = 1 if a[ii] >= b[jj] else 2
            else:
                take = 1 if ii < m else 2

            if take == 1:
                res.append(a[i])
                i += 1
            else:
                res.append(b[j])
                j += 1
    return res

def max_number_from_2_arrays(a, b, k):
    m, n = len(a), len(b)
    max_number = []

    # print min(m + n - k, m)
    # print max(0, k-n), min(m, k)
    for i in range(max(0, k-n), min(m, k) + 1):
        j = k - i
        a_max = max_number_from_array(a, i)
        b_max = max_number_from_array(b, j)

        max_number = max(max_number, merge(a_max, b_max, 0, 0))

    return max_number



class Solution(object):
    def maxNumber(self, nums1, nums2, k):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type k: int
        :rtype: List[int]
        """
        return max_number_from_2_arrays(nums1, nums2, k)

import random
import sys
from utils.templates import fail_string, debug

def unit_test():
    assert max_number_from_array([], 1) == []
    assert max_number_from_array([1], 10) == []
    assert max_number_from_array([9, 1, 8, 5, 6, 3, 4], 3) == [9, 8, 6]
    assert max_number_from_array([8, 8, 8, 8], 2) == [8, 8]

    assert max_number_from_array([9, 1, 8, 5, 6, 3, 4], 7) == [9, 1, 8, 5, 6, 3, 4]
    assert max_number_from_array([9, 1, 8, 9, 8, 5, 6, 3, 4], 7) == [9, 9, 8, 5, 6, 3, 4]

def test():
    solution = Solution()
    for case, ans in [
        ([[9,5,6,2,4,3,6,2], [5,7,6,2,2,1,3,0,2,8,9,7,7,3,2,2,9,4,5,1], 28], [9,5,7,6,5,6,2,4,3,6,2,2,2,1,3,0,2,8,9,7,7,3,2,2,9,4,5,1]),
        ([[4,6,9,1,0,6,3,1,5,2,8,3,8,8,4,7,2,0,7,1,9,9,0,1,5,9,3,9,3,9,7,3,0,8,1,0,9,1,6,8,8,4,4,5,7,5,2,8,2,7,7,7,4,8,5,0,9,6,9,2],
            [9,9,4,5,1,2,0,9,3,4,6,3,0,9,2,8,8,2,4,8,6,5,4,4,2,9,5,0,7,3,7,5,9,6,6,8,8,0,2,4,2,2,1,6,6,5,3,6,2,9,6,4,5,9,7,8,0,7,2,3], 60],
            [9,9,9,9,9,9,9,9,9,9,9,9,9,8,8,6,8,8,4,4,5,7,5,2,8,2,7,7,7,4,8,5,0,9,6,9,2,0,2,4,2,2,1,6,6,5,3,6,2,9,6,4,5,9,7,8,0,7,2,3]),
        ([[8, 9], [3, 9], 3], [9, 8, 9]),
        ([[1,6,5,4,7,3,9,5,3,7,8,4,1,1,4], [4,3,1,3,5,9], 21], [4,3,1,6,5,4,7,3,9,5,3,7,8,4,1,3,5,9,1,1,4]),
        ([[8, 9, 3, 9, 8, 9, 3, 9], [3, 9, 8, 9, 3, 9, 8, 9], 9], [9, 9, 9, 9, 9, 9, 9, 8, 9]),
        ([[1, 1, 9], [1, 1, 9], 3], [9, 1, 9]),
        ([random.sample(range(100000), 100000), random.sample(range(100000), 100000), 20], True),
        # ([random.sample(range(100000), 100000), random.sample(range(100000), 100000), 100000], True),
        ([[1, 2, 9, 3], [1, 2, 9, 3], 2], [9, 9]),
        ([[1, 2, 9, 3], [], 2], [9, 3]),
        ([[], [1, 2, 9, 3], 2], [9, 3]),
        ([[3, 4, 6, 5], [9, 1, 2, 5, 8, 3], 5], [9, 8, 6, 5, 3]),
        ([[6, 7], [6, 0, 4], 5], [6, 7, 6, 0, 4]),
        ([[8, 8, 8], [8, 8, 8, 8], 7], [8, 8, 8, 8, 8, 8, 8]),
    ]:
        res = solution.maxNumber(*case)
        if ans is not True:
            try:
                assert res == ans
            except AssertionError as e:
                status = fail_string(res=res, ans=ans, case=case)
                sys.exit(status)

if __name__ == '__main__':
    test()
    unit_test()