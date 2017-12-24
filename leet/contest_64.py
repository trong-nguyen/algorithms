#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Input: nums = [3, 6, 1, 0]
Output: 1
Explanation: 6 is the largest integer, and for every other number in the array x,
6 is more than twice as big as x.  The index of value 6 is 1, so we return 1.
"""


import sys
from utils.templates import fail_string


def twice(nums):
    idx, largest = 0, nums[0]
    for i, v in enumerate(nums[1:]):
        if v > largest:
            if v < 2 * largest:
                idx = -1
            else:
                idx = i + 1

            largest = v
        elif largest < 2*v:
            idx = -1

        print idx, v, largest
    return idx

def test():
    for case, ans in [
        # ([[3, 6, 1, 0]], 1),
        # ([[1, 2, 3, 4]], -1),
        ([[0,0,3,2]], -1),
    ]:
        res = twice(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()