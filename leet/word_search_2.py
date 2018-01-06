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
"""

EOW = '$' # end of word, conform to regex

def build_trie(words):
    trie = {}
    for word in words:
        t = trie
        for i, c in enumerate(word):
            t[c] = t.get(c, {})
            if i == len(word) - 1:
                t[EOW] = True
            else:
                t = t[c]
    return trie


def word_search(board, words):
    def get_trie_nb(branch):
        return filter(lambda nb: nb != '*', branch.keys())

    def get_board_nb(coord, b):
        m, n = len(b), len(b[0])
        i, j = coord

        def bounded(c):
            return 0 <= c[0] <= m-1 and 0 <= c[1] <= n-1
        return filter(bounded, [(i, j-1), (i, j+1), (i-1, j), (i+1, j)])


    def walk_parallel(trie, b, br, b_visited, path, results):
        if EOW in t[t_node]:
            results.append(' '.join(path))

        keys = trie.keys()
        if len(keys) == 1 and keys == [EOW]:
            return True

        b_nb = get_board_nb(br, b)
        b_nb = filter(lambda x: x not in b_visited, b_nb)

        fully_matched = True
        for nb in b_nb:
            t = board[i][j]
            if t in trie:
                bv = b_visited.union(nb)
                matched = walk_parallel(trie[t], b, nb, bv, path + [tb], results)
                if matched:
                    del trie[t]
                else:
                    fully_matched = False

        return fully_matched

    board_roots = {}
    for i, row in enumerate(board):
        for j, char in enumerate(row):
            board_roots[char] = board_roots.get(char, []) + [(i, j)]

    trie = build_trie(words)

    matched = []

    for trie_root in trie:
        if trie_root in board_roots:
            for board_root in board_roots:
                ws = walk_parallel(trie, trie_root, board, board_root)
                matched += ws

    return set(matched)

    print trie
    print char_indices
    return []


class Solution(object):
    def findWords(self, board, words):
        """
        :type board: List[List[str]]
        :type words: List[str]
        :rtype: List[str]
        """
        return word_search(board, words)


import sys
from utils.templates import fail_string


def test():
    solution = Solution()

    for case, ans in [
        ([[
          ['o','a','a','n'],
          ['e','t','a','e'],
          ['i','h','k','r'],
          ['i','f','l','v']
        ], ["oath","pea","eat","rain"]], ["eat","oath"]),
    ]:
        res = solution.findWords(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()