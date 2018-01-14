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
"""
def create_number(nums1, nums2, i, j, k, mem):
    m, n = len(nums1), len(nums2)
    if m - i + n - j == k:
        res = []
        u, v = i, j
        for ki in range(k):
            if nums1[u] >= nums2[v]:
                res.insert(0, nums1[u])
                u += 1
            else:
                res.insert(0, nums2[v])
                v += 1
        return res

    if i >= m:
        return [0]

    ai, aj = nums1[i], nums2[j]
    if ai >= aj:
        return max([ai] + create_number(nums1, nums2, i+1, j, k-1, mem),
            create_number(nums1, nums2, i, j+1, k))
    else:
        return max([aj] + create_number(nums1, nums2, i, j+1, k-1, mem),
            create_number(nums1, nums2, i+1, j, k))


def create(nums1, nums2, k):
    mem = {}
    return create_number(nums1, nums2, 0, 0, k, mem)


import sys
from utils.templates import fail_string

def test():
    for case, ans in [
        ([[3, 4, 6, 5], [9, 1, 2, 5, 8, 3], 5], [9, 8, 6, 5, 3]),
        ([[6, 7], [6, 0, 4], 5], [6, 7, 6, 0, 4]),
        ([[3, 9], [8, 9], 3], [9, 8, 9]),
    ]:
        res = create(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()