#!/usr/bin/env python
# -*- coding: utf-8 -*-


import math
import sys
from utils.templates import fail_string
import bisect

class Solution(object):
    def is_subsequence(self, word, lookup):
        # print lookup
        if not word:
            return True

        left = -1
        for c in word:
            if c not in lookup:
                return False

            i = bisect.bisect_right(lookup[c], left)
            if i < len(lookup[c]):
                left = lookup[c][i]
            else:
                return False

        return True

    def numMatchingSubseq(self, S, words):
        """
        :type S: str
        :type words: List[str]
        :rtype: int
        """
        lookup = {}
        for i, c in enumerate(S):
            lookup[c] = lookup.get(c, [])
            lookup[c].append(i)

        count = 0
        for word in words:
            if self.is_subsequence(word, lookup):
                count += 1

        return count

class Solution2(object):
    def validTicTacToe(self, board):
        """
        :type board: List[str]
        :rtype: bool
        """
        num_x = 0
        num_o = 0
        for b in board:
            for c in b:
                if c == 'X':
                    num_x += 1
                elif c == 'O':
                    num_o += 1

        if not 0 <= num_x - num_o <= 1:
            return False

        if num_x < 3:
            return True

        rows = board
        cols = [''.join([board[i][j] for i in range(3)]) for j in range(3)]
        diags = [''.join([board[i][i] for i in range(3)]), ''.join([board[i][2-i] for i in range(3)])]

        all_lines = rows + cols + diags
        x_win = 'X'*3 in all_lines
        o_win = 'O'*3 in all_lines

        if x_win:
            return num_x > num_o and not o_win

        if o_win:
            return num_x == num_o

        return not (x_win and o_win)



def unit_test():
    solution = Solution()

    assert solution.numMatchingSubseq("dsahjpjauf", ["ahjpjau","ja","ahbwzgqnuk","tnmlanowax"]) == 2
    assert solution.numMatchingSubseq("qlhxagxdqh", ["qlhxagxdq","qlhxagxdq","lhyiftwtut","yfzwraahab"]) == 2
    assert solution.numMatchingSubseq("abcde", ["a", "bb", "acd", "ace"]) == 3
    assert solution.numMatchingSubseq("abcdbcae", ["a", "bb", "acd", "ace", 'bb', 'bcbc']) == 6


    solution = Solution2()
    assert solution.validTicTacToe(["XXX","XOO","OO "]) == False

    assert solution.validTicTacToe(["XOX","X O","X O"]) == True
    assert solution.validTicTacToe(["O  ", "   ", "   "]) == False
    assert solution.validTicTacToe(["XOX", " X ", "   "]) == False
    assert solution.validTicTacToe(["XXX", "   ", "OOO"]) == False
    assert solution.validTicTacToe(["XOX", "O O", "XOX"]) == True


def test():
    pass

if __name__ == '__main__':
    unit_test()
    test()