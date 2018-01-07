#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given a 2D board and a list of words from the dictionary, find all words in the board.

Each word must be constructed from letters of sequentially adjacent cell, where "adjacent" cells are those horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.

For example,
Given words = ["oath","pea","eat","rain"] and board =

[
  ['o','a','a','n'],
  ['e','t','a','e'],
  ['i','h','k','r'],
  ['i','f','l','v']
]
Return ["eat","oath"].
Note:
You may assume that all inputs are consist of lowercase letters a-z.

SOLUTION:
    - Make use of trie data structures. Basically we try to traverse the board (as a cyclic tree) guided by word trie (another tree)
    - Index (O(n2)) all the cell in the board as potential entry points (roots) to traverse with the trie.
    - For each entry point, traverse 2 trees (board and trie) to find the matched words. This takes O(mk) where m the number of words
        and k the max length of any word.
    - Total: O(mn2k)
    - To improve the efficiency a technique to "burn the bridge" is employed. For each explored branch if the sub branches were matched
        we delete that sub-branch to avoid the possibly repeated searches later.
"""

EOW = '$' # end of word, conform to regex

def build_trie(words):
    """
    Build a simple trie with built in dicts
    """
    trie = {}
    for word in words:
        t = trie
        for i, c in enumerate(word):
            t[c] = t.get(c, {})
            t = t[c]
            if i == len(word) - 1:
                t[EOW] = True # mark it with a EOW
    return trie


def word_search(board, words):
    def get_board_nb(coord, b):
        # get all the neighbors of a specific cell at coord(i, j)
        m, n = len(b), len(b[0])
        i, j = coord

        all_nb = [(i, j-1), (i, j+1), (i-1, j), (i+1, j)]

        if 0 < i < m-1 and 0 < j < n-1:
            # most of the time O(n2) it will not fall on one of the boundaries
            # a quick and optimized check before the filtering (of O(n) elements)
            return all_nb

        def bounded(c):
            return 0 <= c[0] <= m-1 and 0 <= c[1] <= n-1
        return filter(bounded, all_nb)


    def walk_parallel(trie, b, br, b_visited, path, results):
        """
        Given starting roots on trie and board, parallely traverse both trees
        If along the way an EOW is found, add the path travelled to results
        Terminate and burn the branch of trie that was sucessfully explored (no more lower branches)
            to avoid repetitive exploration
        """
        if EOW in trie:
            results.append(''.join(path))
            del trie[EOW]
            if not trie: #dead end
                return True, results

        b_nb = get_board_nb(br, b)
        b_nb = filter(lambda x: x not in b_visited, b_nb)

        for nb in b_nb:
            i, j = nb
            t = board[i][j]
            if t in trie:
                b_visited.add(nb)
                matched, results = walk_parallel(trie[t], b, nb, b_visited, path + [t], results)
                b_visited.remove(nb)

                if matched:
                    del trie[t]

        # the match is complete (all branches matched)
        # if sub trees is empty
        return not trie, results

    board_roots = {}
    for i, row in enumerate(board):
        for j, char in enumerate(row):
            board_roots[char] = board_roots.get(char, []) + [(i, j)]

    trie = build_trie(words)
    found_words = []

    # for each match entry pairs (trie first branches and matching board characters)
    # do the parallel traversals
    trie_roots = trie.keys()
    for trie_root in trie_roots:
        char = trie_root
        if char in board_roots:
            for board_root in board_roots[char]:
                matched, ws = walk_parallel(trie[trie_root], board, board_root, set([board_root]), [trie_root], [])
                found_words += ws
                if matched:
                    # abort other possible entry points if one matched
                    del trie[trie_root]
                    break

    return found_words


class Solution(object):
    def findWords(self, board, words):
        """
        :type board: List[List[str]]
        :type words: List[str]
        :rtype: List[str]
        """
        return word_search(board, words)

import json

def matrix_str(mat):
    return '\n'.join([' '.join(map('{:3}'.format, row)) for row in mat])


import sys
from utils.templates import fail_string


def test():
    solution = Solution()

    for case, ans in [
        ([[["a","b"],["a","a"]], ["aba","baa","bab","aaab","aaa","aaaa","aaba"]], ["aaa","aaab","aaba","aba","baa"]),

        ([[["a","a"]], ["aaa"]], []),

        ([["a"], ["a"]], ["a"]),

        ([[
          ['o','a','a','n'],
          ['e','t','a','e'],
          ['i','h','k','r'],
          ['i','f','l','v']
        ], ["aaa","a","aa", "aaakl"]], ['a', 'aa', 'aaakl', 'aaa']),

        ([[
          ['o','a','a','n'],
          ['e','t','a','e'],
          ['i','h','k','r'],
          ['i','f','l','v']
        ], ["aaa","a","aa","aaaao", "aaaaoe"]], ['a', 'aa', 'aaa']),

        ([[
          ['o','a','a','n'],
          ['e','t','a','e'],
          ['i','h','k','r'],
          ['i','f','l','v']
        ], ["aaa","aat","ahk","erv", "eee", "eakl"]], ['aat', 'erv', 'eakl', 'aaa']),

        ([[
          ['o','a','a','n'],
          ['e','t','a','e'],
          ['i','h','k','r'],
          ['i','f','l','v']
        ], ["oaan","oaaa","oateihkaa","vlkr", "vrkl"]], ['vrkl', 'oaaa', 'oaan', 'oateihkaa', 'vlkr']),

        ([[
          ['o','a','a','n'],
          ['e','t','a','e'],
          ['i','h','k','r'],
          ['i','f','l','v']
        ], ["oath","pea","eat","rain"]], ['oath', 'eat']),

        ([[
          ['o','a','a','n'],
          ['e','t','a','e'],
          ['i','h','k','r'],
          ['i','f','l','v']
        ], ["oath","oate","teoa","rain", "if", "oei", "oaanervlfiie"]], ['oaanervlfiie', 'teoa', 'oate', 'oei', 'oath', 'if']),
    ]:
        print matrix_str(case[0])
        res = solution.findWords(*case)
        try:
            assert sorted(res) == sorted(ans)
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()