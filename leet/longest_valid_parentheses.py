#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given a string containing just the characters '(' and ')', find the length of the longest valid (well-formed) parentheses substring.

For "(()", the longest valid parentheses substring is "()", which has length = 2.

Another example is ")()())", where the longest valid parentheses substring is "()()", which has length = 4.
"""

import sys
from utils.templates import fail_string

def longest_parentheses(s):
    return 2

def test():
    for case, ans in [
        ([')()())'], 4)
    ]:
        res = longest_parentheses(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()