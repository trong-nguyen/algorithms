#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given a string S, you are allowed to convert it to a palindrome by adding characters in front of it. Find and return the shortest palindrome you can find by performing this transformation.

For example:

Given "aacecaaa", return "aacecaaa".

Given "abcd", return "dcbabcd".
"""

def knuth_morris_pratt(s):
    return 's'

import sys
from utils.templates import fail_string

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
    test()