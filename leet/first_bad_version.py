#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

# The isBadVersion API is already defined for you.
# @param version, an integer
# @return a bool
# def isBadVersion(version):

class Solution(object):
    def __init__(self, bad):
        self.bad = bad

    def isBadVersion(self, x):
        return x >= self.bad

    def firstBadVersion(self, n):
        """
        :type n: int
        :rtype: int
        """

        lower_bound = 1
        upper_bound = n

        while lower_bound < upper_bound:
            m = lower_bound + (upper_bound - lower_bound) / 2

            if self.isBadVersion(m):
                upper_bound = m
            else:
                lower_bound = m + 1

        return lower_bound

import sys
from utils.templates import fail_string


def test():
    for case in range(1, 1000):
        for bad in range(1, case):
            solution = Solution(bad)
            ans = bad
            res = solution.firstBadVersion(case)
            try:
                assert res == ans
            except AssertionError as e:
                status = fail_string(res=res, ans=ans, case=case)
                sys.exit(status)

if __name__ == '__main__':
    test()