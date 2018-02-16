#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Find third, non-duplicated largest number
"""
def shift_values_back(a, lim):
    """
    a[lim] will be copied into a[lim-1] and go on
    """
    for i in range(lim):
        a[i] = a[i + 1]

class Solution(object):
    def thirdMax(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        target = 3
        target_basket = set()

        i = 0
        while i < len(nums) and len(target_basket) < target:
            target_basket.add(nums[i])
            i += 1

        target_basket = sorted(list(target_basket))
        while i < len(nums):
            x = nums[i]
            j = 0
            while j < target and x > target_basket[j]:
                j += 1

            if j == target:
                shift_values_back(target_basket, j - 1)
                target_basket[j - 1] = x
            # x can only be <= xj
            elif j == 0 or x == target_basket[j]:
                pass
            else:
                shift_values_back(target_basket, j - 1)
                target_basket[j - 1] = x

            i += 1

        if len(target_basket) < target:
            return target_basket[-1]
        else:
            return target_basket[0]

import random
import sys
from utils.templates import fail_string

def unit_test():
    array = [1, 2, 3, 4]
    shift_values_back(array, 2)
    assert array == [2, 3, 3, 4]

def test():
    solution = Solution()
    for case, ans in [
        ([3, 2, 1], 1),
        ([1, 2], 2),
        ([2, 2, 3, 1], 1),
        ([4, 1, 7, 9, 8, 6, 0, 3, 5, 2], 7),
        ([random.choice(range(20)) for i in range(100)], True),
        (random.sample(range(10), 10), True),
        (random.sample(range(100000), 100000), True),
    ]:
        if ans is True:
            sorted_case = sorted(set(case))
            if len(sorted_case) < 3:
                ans = sorted_case[-1]
            else:
                ans = sorted_case[-3]

        res = solution.thirdMax(case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    unit_test()
    test()