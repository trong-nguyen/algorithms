#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given a string S, you are allowed to convert it to a palindrome by adding characters in front of it. Find and return the shortest palindrome you can find by performing this transformation.

For example:

Given "aacecaaa", return "aacecaaa".

Given "abcd", return "dcbabcd".
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

def build_failure_table(w):
    if not w:
        return []

    table = [-1] + [0] * (len(w) - 1)
    for i in range(1, len(w)):

        d = table[i-1]
        if w[i-1] == w[d]:
            table[i] = table[i-1] + 1


    return table

def second_sweep(w, table):
    def satisfied(i, d, w):
        return w[i] != w[d] and w[i-d:i] == w[:d]

    # now checking w[i] which have boolean values (i.e. t[i]
    # corresponding to s[i] being not w[i])
    for i in range(1, len(w)):
        d = table[i]

        if w[i] == w[d]:
            if d == 0:
                table[i] = -1
            else:
                for j in range(d-1, -1, -1):
                    if satisfied(i, j, w):
                        table[i] = j
                        break
                    elif j == 0: # if not satisfied even when j=0
                        table[i] = -1


    return table

def third_sweep(w, table):
    def satisfied(i, d, w):
        return w[i] != w[d] and w[i-d:i] == w[:d]

    # now checking w[i] which have boolean values (i.e. t[i]
    # corresponding to s[i] being not w[i])
    for i in range(1, len(w)):
        d = table[i-1]

        if d > table[i]:
            for j in range(d-1, -1, -1):
                if satisfied(i, j, w):
                    table[i] = j
                    break


    return table

def knuth_morris_pratt(s):
    return 's'

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