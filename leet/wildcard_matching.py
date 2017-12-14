#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implement wildcard pattern matching with support for '?' and '*'.

'?' Matches any single character.
'*' Matches any sequence of characters (including the empty sequence).

The matching should cover the entire input string (not partial).

The function prototype should be:
bool isMatch(const char *s, const char *p)

Some examples:
isMatch("aa","a") → false
isMatch("aa","aa") → true
isMatch("aaa","aa") → false
isMatch("aa", "*") → true
isMatch("aa", "a*") → true
isMatch("ab", "?*") → true
isMatch("aab", "c*a*b") → false
"""

import sys
from utils import fail_string

def test():
    for case, ans in [
    ]:
        res = function(*case)
        try:
            assert res == ans
        except AssertionError as e:
            sys.exit(fail_string(res=res, ans=ans))

if __name__ == '__main__':
    test()