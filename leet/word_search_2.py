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
        if not trie:
            return True, results

        b_nb = get_board_nb(br, b)
        b_nb = filter(lambda x: x not in b_visited, b_nb)
        # print '\t', b_nb

        for nb in b_nb:
            i, j = nb
            t = board[i][j]
            if t in trie:
                bv = b_visited.union(nb)
                matched, results = walk_parallel(trie[t], b, nb, bv, path + [t], results)
                if EOW in trie:
                    results += [''.join(path + [t])]

                if matched:
                    del trie[t]

        # the match is complete (all branches matched)
        # if sub trees is empty
        if EOW in trie:
            return len(trie) == 1, results
        else:
            return not trie, results

    board_roots = {}
    for i, row in enumerate(board):
        for j, char in enumerate(row):
            board_roots[char] = board_roots.get(char, []) + [(i, j)]

    trie = build_trie(words)

    found_words = []

    trie_roots = trie.keys()
    for trie_root in trie_roots:
        char = trie_root
        if char in board_roots:
            if not trie[trie_root]: # single word
                found_words.append(char)
            else:
                for board_root in board_roots[char]:
                    matched, ws = walk_parallel(trie[trie_root], board, board_root, set([board_root]), [trie_root], [])
                    found_words += ws
                    if matched:
                        # abort other possible entry points if one matched
                        del trie[trie_root]
                        break

                    # print trie

    return list(set(found_words))


class Solution(object):
    def findWords(self, board, words):
        """
        :type board: List[List[str]]
        :type words: List[str]
        :rtype: List[str]
        """
        return word_search(board, words)

def matrix_str(mat):
    return '\n'.join([' '.join(map('{:3}'.format, row)) for row in mat])


import sys
from utils.templates import fail_string


def test():
    solution = Solution()

    for case, ans in [
        ([[["a","a"]], ["aaa"]], []),

        ([["a"], ["a"]], ["a"]),

        ([[
          ['o','a','a','n'],
          ['e','t','a','e'],
          ['i','h','k','r'],
          ['i','f','l','v']
        ], ["aaa","a","aa", "aaakl"]], ['aa', 'aaakl', 'aaa']),

        ([[
          ['o','a','a','n'],
          ['e','t','a','e'],
          ['i','h','k','r'],
          ['i','f','l','v']
        ], ["aaa","a","aa","aaaao", "aaaaoe"]], ['aa', 'aaa']),

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
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()