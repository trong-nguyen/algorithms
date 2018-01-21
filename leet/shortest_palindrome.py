#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given a string S, you are allowed to convert it to a palindrome by adding characters in front of it. Find and return the shortest palindrome you can find by performing this transformation.

For example:

Given "aacecaaa", return "aacecaaa".

Given "abcd", return "dcbabcd".

SOLUTION:
    The problem can be solved naively in O(n2) by searching for longest palindromes starting at index 0
    Doing some research on Knuth-Morris-Pratt suggests a linear O(n) time solution
    The central idea is to create an efficient and clever "backtracking" system based on not one
    but an array of information. In this case, that array is the entire word.

    Think about it, the naive solution progresses linearly and each time takes linear effort to search
    for a possible palindrome.

    The KMP improves by accelerating the progresses significantly. Intuitively, it is clear that in the naive
    solution we scan the array over and over again only differ by a single character. Just like you go through
    a street repetitively each time looking for a different item. It could be much more efficient that we have a
    list of items to search for before hand. By that way in the process of looking for item i we take note that
    we encountered / didnot encounter item j so that we don't need to go backward just to browse through the old
    information again looking for item j. This technique can only be made possible if we planned that we are going
    to search for item i and j (and possibly k, l, m).

    Algorithm:
        - The KMP solution requires to build a failure table T[i] that has the same size of the search word W
        - So that on searching the string S for the word W, we already know what we are and are not looking for
        - Assume that at index i on the the string S the match begins up to index j, instead of going back to index
        i + 1 looking for word W, which by the way matched from index 0 to index j W[0:j], we can consult table T at
        position i T[i] to: continue on to index j + 1 knowing that if there is a sub pattern within W[0:k] we can match
        against the S[l:l+k] where i < l and k < j. The index k was precomputed in the failure table T just by accessing T[j]
        - The actual brilliant algorithm can only be explained by sliding the same W against itself looking for the so called
        longest proper suffix which at the same time profer prefix of the word considered up to index j W[0:j]

        - Then after having the failure table, the shortest palindrome problem can be solved cleverly by
        search for word W on the inverse of itself W[::-1]. This will result in the longest match between the suffix of the
        inverse of W and W which at worst case, will at least match at W[::-1][-1] since of course abc[0] == abc[::-1][-1]
        W[::-1]:    --------x
        W:                  x--------

        - But in other cases it might matches some where in the middle for example
        W[::-1]:    ----xyzkzyx
        W:              xyzkzyx----

        - Look at the algorithm, think about it and read more about Knuth-Morris-Pratt to enlighten yourself.

"""

def slide_build_table(w):
    if not w:
        return []

    table = [-1] + [0] * (len(w) - 1)

    j = 0
    for i in range(1, len(w)):
        if w[i] == w[j]:
            table[i] = table[j]
            j += 1
        else:
            table[i] = j
            # reset j jumping until find the closest w[i] prior to j
            while True:
                j = table[j]
                if w[i] == w[j] or j < 0:
                    break
            j += 1
    return table

def search(s, w, table):
    i = 0
    j = 0

    for i in range(len(s)):
        if s[i] == w[j]:
            j += 1
        else:
            j = table[j]
            j += 1

    return s + w[j:]

def build_shortest_palindrome(w):
    t = slide_build_table(w)
    return search(w[::-1], w, t)

class Solution(object):
    def shortestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        return build_shortest_palindrome(s)

import sys
from utils.templates import fail_string

def unit_test():
    def aligned_str(array, room=3):
        return ' '.join(map('{{:>{}}}'.format(room).format, array))

    w = 'ABCDABD'
    t = slide_build_table(w)
    assert t == [-1, 0, 0, 0, -1, 0, 2]
    # t = build_failure_table(w)
    # print aligned_str(w)
    # print aligned_str(t)
    # t = third_sweep(w, t)
    # print aligned_str(t)
    # print aligned_str(second_sweep(w, t))
    # print aligned_str(slide_build_table(w))-1 0   0   0   0   0   0   -1  0   2   0   0   0   0   0   -1  0   0   3   0   0   0   0   0

    w = 'ABACABABC'
    t = slide_build_table(w)
    assert t == [-1, 0, -1, 1, -1, 0, -1, 3, 2]
    # t = build_failure_table(w)
    # print aligned_str(w)
    # print aligned_str(t)
    # t = third_sweep(w, t)
    # print aligned_str(t)
    # print aligned_str(second_sweep(w, t))
    # print aligned_str(slide_build_table(w))-1 0   0   0   0   0   0   -1  0   2   0   0   0   0   0   -1  0   0   3   0   0   0   0   0

    w = 'PARTICIPATE IN PARACHUTE'
    t = slide_build_table(w)
    assert t == [-1, 0, 0, 0, 0, 0, 0, -1, 0, 2, 0, 0, 0, 0, 0, -1, 0, 0, 3, 0, 0, 0, 0, 0]
    # t = build_failure_table(w)
    # print aligned_str(w)
    # print aligned_str(t)
    # t = third_sweep(w, t)
    # print aligned_str(t)
    # print aligned_str(second_sweep(w, t))
    # print aligned_str(slide_build_table(w))-1 0   0   0   0   0   0   -1  0   2   0   0   0   0   0   -1  0   0   3   0   0   0   0   0

    n = 1000000
    w = 'X' * n
    t = slide_build_table(w)
    assert t == [-1] * n
    # t = build_failure_table(w)
    # print aligned_str(w)
    # print aligned_str(t)
    # t = third_sweep(w, t)
    # print aligned_str(t)
    # print aligned_str(second_sweep(w, t))
    # print aligned_str(slide_build_table(w))-1 0   0   0   0   0   0   -1  0   2   0   0   0   0   0   -1  0   0   3   0   0   0   0   0


    print aligned_str('aaacecaa')
    print aligned_str(slide_build_table('aaacecaa'))
    print '\n'

    w = 'AABBA'
    s = w[::-1]
    t = slide_build_table(w)
    print aligned_str(search(s, w, t))
def test():
    solution = Solution()
    for case, ans in [
        (["aabba"], "abbaabba"),
        (['aea'], 'aea'),
        (['a'], 'a'),
        ([''], ''),
        (['aacecaaa'], 'aaacecaaa'),
        (['abcd'], 'dcbabcd'),
        (['xxx'*1000 + 'y' + 'xxx'*1000], 'xxx'*1000 + 'y' + 'xxx'*1000),
        (['xxx'*1000], 'xxx'*1000),
    ]:
        res = solution.shortestPalindrome(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    unit_test()
    test()