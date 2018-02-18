#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import sys
from utils.templates import fail_string

class Solution(object):
    def findPairs(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        if k < 0:
            return 0

        lookup = set()
        counted = set()
        count = 0
        for x in nums:
            for y in (x + k, x - k):
                if y in lookup and (x, y) not in counted:
                    count += 1
                    counted.add((x, y))
                    counted.add((y, x))
            lookup.add(x)

        return count



def test():
    solution = Solution()
    for case, ans in [
        ([[3, 1, 4, 1, 5], 2], 2),
        ([[1, 2, 3, 4, 5], 1], 4),
        ([[1, 3, 1, 5, 4], 0], 1),
    ]:
        res = solution.findPairs(*case)
        if ans is True:
            # we just want to test the algorithm on random inputs
            print res
            continue

        if ans is None:
            # we have a bruteforce algorithm to test against
            ans = bruteforce
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()