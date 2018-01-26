#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
There are N children standing in a line. Each child is assigned a rating value.

You are giving candies to these children subjected to the following requirements:

Each child must have at least one candy.
Children with a higher rating get more candies than their neighbors.
What is the minimum candies you must give?
"""

def count_non_decreasing(ratings, i):
    ci = 1
    candies = 1

    i0 = i
    while i + 1 < len(ratings) and ratings[i+1] >= ratings[i]:
        ci += (1 if ratings[i+1] > ratings[i] else 0)
        candies += ci
        i += 1

    if i > i0 and i < len(ratings) - 1:
        candies -= ci

    return i, ci, candies

def count_non_increasing(ratings, i, c0):
    ci = c0
    candies = c0

    i0 = i
    while i + 1 < len(ratings) and ratings[i+1] <= ratings[i]:
        ci -= (1 if ratings[i+1] < ratings[i] else 0)
        candies += ci
        i += 1

    shift = 1 - ci
    candies += shift * (i - i0)

    if shift > 0:
        j = i0
        while j >= 0 and ratings[j] == ratings[i0]:
            candies += shift
            j -= 1

    if i > i0 and i < len(ratings) - 1:
        candies -= 1

    return i, 1, candies

def give_candy(ratings):
    n = len(ratings)
    if n == 0:
        return 0
    if n == 1:
        return 1

    positive = ratings[1] >= ratings[0]

    i = 0
    c0 = 1
    candies = 0
    recorded = []
    while i + 1 < n:
        if positive:
            i, c0, csum = count_non_decreasing(ratings, i)
            recorded.append(csum)
            # print 'positive', i
        else:
            i, c0, csum = count_non_increasing(ratings, i, c0)
            recorded.append(-csum)
            # print 'negative', i

        positive = not positive
        candies += csum

    # print recorded
    return candies

def give_illogical_candies(ratings):
    n = len(ratings)
    if n == 0:
        return 0
    if n == 1:
        return 1


    lcandies = [1] * n
    rcandies = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i-1]:
            lcandies[i] = lcandies[i-1] + 1

    for i in range(n-2, -1, -1):
        if ratings[i] > ratings[i+1]:
            rcandies[i] = rcandies[i+1] + 1

    candies = [1] * n
    candies[0] = rcandies[0]
    candies[-1] = lcandies[-1]

    for i in range(1, n - 1):
        candies[i] = max(lcandies[i], rcandies[i])

    # print candies
    return sum(candies)

class Solution(object):
    def candy(self, ratings):
        """
        :type ratings: List[int]
        :rtype: int
        """
        # return give_candy(ratings)
        return give_illogical_candies(ratings)

import random
import sys
from utils.templates import fail_string

def test():
    solution = Solution()
    for case, ans in [
        ([[1, 2, 2]], 4),
        ([[]], 0),
        ([[1e6]], 1),
        ([[1, 100]], 3),
        ([[1000, 100]], 3),
        ([[0, 1, 0, 2, 0, 3, 0, 4]], 12),
        ([[1, 10, 2]], 4),
        ([[1, 3, 2, 4]], 6),
        ([[1, 10, 11, 1]], 7),
        ([[10, 8, 1, 2, 4, 5, 4, 1, 0, -1, -2]], 32),
        # ([random.sample(range(100000), 100000)], True),
    ]:
        # print case
        res = solution.candy(*case)
        if ans is not True:
            try:
                assert res == ans
            except AssertionError as e:
                status = fail_string(res=res, ans=ans, case=case)
                sys.exit(status)

if __name__ == '__main__':
    test()