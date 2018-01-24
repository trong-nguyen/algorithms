#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
There are N children standing in a line. Each child is assigned a rating value.

You are giving candies to these children subjected to the following requirements:

Each child must have at least one candy.
Children with a higher rating get more candies than their neighbors.
What is the minimum candies you must give?
"""

def count_non_decreasing(ratings, i0, c0):
    candies = 0
    i = i0
    ci = c0
    while i < len(ratings) and ratings[i] >= ratings[i-1]:
        ci = ci + (1 if ratings[i] > ratings[i-1] else 0)
        candies += ci
        i += 1

    if i > i0:
        candies -= ci

    return i, ci, candies

def count_non_increasing(ratings, i0, c0):
    candies = 0
    i = i0
    ci = c0
    while i < len(ratings) and ratings[i] <= ratings[i-1]:
        ci = ci - (1 if ratings[i] < ratings[i-1] else 0)
        candies += ci
        i += 1

    candies -= (candies - 1) * (i - i0)

    return i, ci, candies

def give_candy(ratings):
    n = len(ratings)
    if n == 0:
        return 0
    if n == 1:
        return 1

    c0 = 1
    i = 0
    candies = 0
    while i < n:
        i, c0, csum = count_non_decreasing(ratings, i, c0)
        candies += csum
        i, c0, csum = count_non_increasing(ratings, i, c0)
        candies += csum

    return candies

class Solution(object):
    def candy(self, ratings):
        """
        :type ratings: List[int]
        :rtype: int
        """
        return give_candy(ratings)

import sys
from utils.templates import fail_string

def test():
    solution = Solution()
    for case, ans in [
        ([[1, 3, 2, 4]], 6),
        ([[1, 10, 11, 1]], 7),
        ([[10, 8, 1, 2, 4, 5, 4, 1, 0, -1, -2]], 30),
    ]:
        res = solution.candy(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()