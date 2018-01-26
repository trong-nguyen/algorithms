#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given integers n and k, find the lexicographically k-th smallest integer in the range from 1 to n.

Note: 1 ≤ k ≤ n ≤ 109.

Example:

Input:
n: 13   k: 2

Output:
10

Explanation:
The lexicographical order is [1, 10, 11, 12, 13, 2, 3, 4, 5, 6, 7, 8, 9], so the second smallest number is 10.
"""

def k_lexico(n, k):
    return 1



class Solution(object):
    def findKthNumber(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """
        return k_lexico(n, k)

import sys
from utils.templates import fail_string

def test():
    solution = Solution()
    for case, ans in [
        ([2, 2], 2),
        ([10, 3], 2),
        ([1, 1], 1),
        ([13, 2], 10),
    ]:
        res = solution.findKthNumber(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()