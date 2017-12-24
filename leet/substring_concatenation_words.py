#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
You are given a string, s, and a list of words, words, that are all of the same length. Find all starting indices of substring(s) in s that is a concatenation of each word in words exactly once and without any intervening characters.

For example, given:
s: "barfoothefoobarman"
words: ["foo", "bar"]

You should return the indices: [0,9].
(order does not matter).
"""

import sys
from utils.templates import fail_string

def subcon(string, words):
    """
    Substring concatenation
    """
    return 1

def test():
    for case, ans in [
        (["a"*10, ["a"]], list(range(9))),
        (["ababab", ["a", "b"]], [0, 1, 2, 3, 4]),
        (["aabbaabb", ["a", "a"]], [0, 4]),
        (["barfoothefoobarman", ["foo", "bar"]], [0,9]),
        (["fobafo", ["fo", "ba"]], [0, 2]),
    ]:
        res = subcon(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()