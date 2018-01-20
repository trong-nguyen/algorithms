#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given a string S, you are allowed to convert it to a palindrome by adding characters in front of it. Find and return the shortest palindrome you can find by performing this transformation.

For example:

Given "aacecaaa", return "aacecaaa".

Given "abcd", return "dcbabcd".
"""

def build_failure_table(w):
    if not w:
        return []

    table = [-1] + [0] * (len(w) - 1)
    for i in range(2, len(w)):
        # if table[i-1] == 0:
        #     if w[i] == w[0]:
        #         table[i] = -1
        #     elif w[i-1] == w[0]:
        #         table[i] = 1
        # else:
        #     d = i - 1 - table[i-1]
        #     if w[i-1] == w[i-d-1]:
        #         table[i] = table[i-1] + 1

        d = i - 1 - table[i-1]
        if w[i-1] == w[i-d-1]:
            table[i] = table[i-1] + 1

    # now checking w[i] which have boolean values (i.e. t[i]
    # corresponding to s[i] being not w[i])
    for i in range(2, len(w)):
        while w[i] == w[table[i]] and table[i] >= 0:
            table[i] -= 1

    return table

def knuth_morris_pratt(s):
    return 's'

import sys
from utils.templates import fail_string

def unit_test():
    def aligned_str(array, room):
        return ' '.join(map('{{:>{}}}'.format(room).format, array))

    spaces = 3
    w = 'ABCDABD'
    t = build_failure_table(w)
    print aligned_str(w, 3)
    print aligned_str(t, 3)
    print '\n'

    w = 'ABACABABC'
    t = build_failure_table(w)
    print aligned_str(w, 3)
    print aligned_str(t, 3)
    print '\n'

    w = 'PARTICIPATE IN PARACHUTE'
    t = build_failure_table(w)
    print aligned_str(w, 3)
    print aligned_str(t, 3)
    print '\n'

def test():
    for case, ans in [
        (['aacecaaa'], 'aacecaaa'),
        (['abcd'], 'dcbabcd'),
    ]:
        res = knuth_morris_pratt(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    unit_test()
    test()