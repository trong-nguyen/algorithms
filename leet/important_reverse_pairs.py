#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given an array nums, we call (i, j) an important reverse pair if i < j and nums[i] > 2*nums[j].

You need to return the number of important reverse pairs in the given array.

Example1:

Input: [1,3,2,3,1]
Output: 2
Example2:

Input: [2,4,3,5,1]
Output: 3
Note:
The length of the given array will not exceed 50,000.
All the numbers in the input array are in the range of 32-bit integer.

"""

import sys
from utils import fail_string

def reverse_pairs(nums):
    """
    """
    # sort, keeping the order
    array = sorted(enumerate(nums), cmp=lambda a, b: a[0] <= b[0] and a[1] > 2 * b[1])

    # iterate and count
    pairs = 0
    for i in range(len(array) - 1):


    # count the one that satisfy order and mag conditions


class Solution(object):
    def reversePairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """


def test():
    for case, ans in [
        ([[1,3,2,3,1]], 2),
        ([[2,4,3,5,1]], 3),
    ]:
        res = function(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()