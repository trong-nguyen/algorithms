#!/usr/bin/env python
# -*- coding: utf-8 -*-


import math
import sys
from utils.templates import fail_string
import bisect


class Solution2(object):
    def allPathsSourceTarget(self, graph):
        """
        :type graph: List[List[int]]
        :rtype: List[List[int]]
        """
        n = len(graph)
        mem = {}
        deadend = set()
        def traverse(i):

            if i == n - 1:
                return [[i]]

            if i in mem:
                return mem[i]

            nb = [j for j in graph[i] if j not in deadend]
            if not nb:
                deadend.add(i)
                return []

            suffixes = []
            for j in nb:
                suffixes += traverse(j)

            if not suffixes:
                deadend.add(i)
                return []

            mem[i] = [[i] + suffix for suffix in suffixes]
            return mem[i]

        traverse(0)
        return mem[0]



class Solution1(object):
    def rotateString(self, A, B):
        """
        :type A: str
        :type B: str
        :rtype: bool
        """
        return A in B * 2


class Solution(object):
    """
    We stack glasses in a pyramid, where the first row has 1 glass, the second row has 2 glasses, and so on until the 100th row.  Each glass holds one cup (250ml) of champagne.

    Then, some champagne is poured in the first glass at the top.  When the top most glass is full, any excess liquid poured will fall equally to the glass immediately to the left and right of it.  When those glasses become full, any excess champagne will fall equally to the left and right of those glasses, and so on.  (A glass at the bottom row has it's excess champagne fall on the floor.)

    For example, after one cup of champagne is poured, the top most glass is full.  After two cups of champagne are poured, the two glasses on the second row are half full.  After three cups of champagne are poured, those two cups become full - there are 3 full glasses total now.  After four cups of champagne are poured, the third row has the middle glass half full, and the two outside glasses are a quarter full, as pictured below.



    Now after pouring some non-negative integer cups of champagne, return how full the j-th glass in the i-th row is (both i and j are 0 indexed.)



    Example 1:
    Input: poured = 1, query_glass = 1, query_row = 1
    Output: 0.0
    Explanation: We poured 1 cup of champange to the top glass of the tower (which is indexed as (0, 0)). There will be no excess liquid so all the glasses under the top glass will remain empty.

    Example 2:
    Input: poured = 2, query_glass = 1, query_row = 1
    Output: 0.5
    Explanation: We poured 2 cups of champange to the top glass of the tower (which is indexed as (0, 0)). There is one cup of excess liquid. The glass indexed as (1, 0) and the glass indexed as (1, 1) will share the excess liquid equally, and each will get half cup of champange.


    Note:

    poured will be in the range of [0, 10 ^ 9].
    query_glass and query_row will be in the range of [0, 99].

    Solution:
        O(n^2): iterate at most n row each at most n glasses

        This is an epic yet beautiful illustration for the power of computational algorithms vs
        math formulation. I tried to model the spilling process in math to no avail. So sophisticated.
        Yet with just a recursive approach, the problem reveals itself naturally.

        The amount of liquid in an arbitrary cup can only be poured down from its parent.
        Lets call them left and righ parent. Special cases are when at the edge where we only have one parent.
        Then the main recursive formulation is:
        amount at (row, glass) = (amount from left (row-1, glass-1) - 1) / 2
            + (amount from right at (row-1, glass) - 1) / 2

        the amounts are limited to non-negative numbers, which mean no liquid from that side
        Done!
    """
    def champagneTower(self, poured, query_row, query_glass):
        """
        :type poured: int
        :type query_row: int
        :type query_glass: int
        :rtype: float
        """

        spill = {}
        def liquid_spilled_out_of(row, glass):
            if row == 0:
                return poured

            for rg in [(row, glass), (row, row - glass)]:
                if rg in spill:
                    return spill[rg]

            if glass > 0:
                from_left = liquid_spilled_out_of(row - 1, glass - 1) - 1
                from_left = max(from_left / 2., 0.0)
            else:
                from_left = 0.0

            if glass == row:
                from_right = 0.0
            else:
                from_right = liquid_spilled_out_of(row - 1, glass) - 1
                from_right = max(from_right / 2., 0.0)

            # print '[{}, {}]: left {}, right {}'.format(row, glass, from_left, from_right)
            amount = from_left + from_right

            spill[(row, glass)] = amount
            return amount

        amount_at_query_glass = liquid_spilled_out_of(query_row, query_glass)

        # print spill
        return min(amount_at_query_glass, 1.0)


def unit_test():
    solution = Solution()
    for case, ans in [
        [(4, 2, 2), 0.25],
        [(4, 2, 1), 0.5],
        [(1, 1, 1), 0.0],
        [(2, 1, 1), 0.5],
        [(100, 1, 1), 1.0],
        # [(1000000000, 99, 88), 1.0],
    ]:
        res = solution.champagneTower(*case)
        assert res == ans, 'Res {}, Expected {}'.format(res, ans)



    solution = Solution2()
    print solution.allPathsSourceTarget([[1,2], [3], [3], []])


    solution = Solution1()

    assert solution.rotateString('abcde', 'cdeab') == True
    assert solution.rotateString('abcde', 'abced') == False

def test():
    pass

if __name__ == '__main__':
    unit_test()
    test()