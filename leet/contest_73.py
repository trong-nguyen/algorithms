#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Solution(object):
    """
    We have two types of tiles: a 2x1 domino shape, and an "L" tromino shape. These shapes may be rotated.

    XX  <- domino

    XX  <- "L" tromino
    X
    Given N, how many ways are there to tile a 2 x N board? Return your answer modulo 10^9 + 7.

    (In a tiling, every square must be covered by a tile. Two tilings are different if and only if there are two 4-directionally adjacent cells on the board such that exactly one of the tilings has both squares occupied by a tile.)

    Example:
    Input: 3
    Output: 5
    Explanation:
    The five different ways are listed below, different letters indicates different tiles:
    XYZ XXZ XYY XXY XYY
    XYZ YYZ XZZ XYY XXY

    SOLUTION: I have to admit that this is a very beautiful problem

    It is a nice combination of dynamic programming and abstract geometry thinking

    These are the observations neccessary to solve:
    - There are odd and even tiles (tromino and vertical domino are odd tiles,
    while horizontal domino is even)
    - Tiling is vertical symmetry (there are 2 ways to arrange trominos to a 2*3 board)
    - If we fill a number of cells, the remained cells can also be filled recursively
    - Do not rush to combine 2 trominos into even cells, there must be an even number of trominos,
    but they do not need to fit next to each other. Look at this 2*7 example
        xx bb dd y
        x aa cc yy

    So, let's use observation 3 as the base for dynamic calculation, starting from the left:

    A. If we have a flat wall on the left (imagine the previous nicely fit together) then we can fill
    next by a:
        + A tromino: 2 ways (up or down)        and the board size reduced by 1.5
        + 2 horizontal stacking domino: 1 way   and the board size reduced by 2
        + 1 vertical domino                     and the board size reduced by 1

    B. If we have a protruded wall on the left (imagin previously we filled a tromino either up or down),
    then we can either fill next by a:
        + A tromino: 1 way (must fit to the previous)               and the board size reduced by 1.5
        + A horizontal domino: 1 way (fit to the un-protruded cell) and the board size reduced by 1

    Note that we use fractional numbers to represent oddly adding a tromino. And conveniently,
    to distingush between case A (N is a whole / integer number) and B (N is a fraction / float number)


    Cost: we have to add all possibilities and the slowest dimension reduction is 1 unit (add a vertical domino).
    So it will be of O(N) cost.
    """

    def __init__(self):
        self.cache = {
            1   : 1,
            1.5 : 1,
            2   : 2, # actually cache max of 2 is sufficient
            2.5 : 2,
            3   : 5,
            3.5 : 4,
            4   : 11
        }


    def numTilings(self, N):
        """
        :type N: int
        :rtype: int
        """
        if N in self.cache:
            return self.cache[N]

        if type(N) is int:
            res = (2 * self.numTilings(N - 1.5) +
                self.numTilings(N - 2) +
                self.numTilings(N - 1))
        else:
            res = self.numTilings(int(N - 1.5)) + self.numTilings(N - 1)

        res %= 1000000007

        self.cache[N] = res

        return res


class Solution2(object):
    def customSortString(self, S, T):
        """
        :type S: str
        :type T: str
        :rtype: str
        """
        t_lookup = {}
        for c in T:
            t_lookup[c] = t_lookup.get(c, 0) + 1

        res = ''
        for c in S:
            res += c * t_lookup[c]
            del t_lookup[c]

        for c in t_lookup:
            res += c * t_lookup[c]

        return res



import math
import sys
from utils.templates import fail_string

def unit_test():
    pass

def test():
    solution = Solution()
    for i in range(1, 100):
        print i, solution.numTilings(i)



    solution = Solution2()
    print solution.customSortString("cba", "abcd")

    print solution.customSortString("cba", "ccabba")

if __name__ == '__main__':
    unit_test()
    test()