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
        return x == self.bad

    def firstBadVersion(self, n):
        """
        :type n: int
        :rtype: int
        """

        if self.isBadVersion(1):
            return 1

        jump = (n + 1) / 2
        version = 1
        while True:
            if self.isBadVersion(version):
                if not self.isBadVersion(version - 1):
                    return version
                else:
                    version = max(version - jump, 1)
            else:
                # if version == n - 1:
                #     return n

                version = min(version + jump, n)


            if jump == 1:
                break
            else:
                jump = (jump + 1) / 2

        raise Exception('Error jumping')

import sys
from utils.templates import fail_string


def test():
    for case in range(5, 6):
        for bad in range(1, case):
            print 'cb', case, bad
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