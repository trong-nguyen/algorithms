#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.

For example,
"A man, a plan, a canal: Panama" is a palindrome.
"race a car" is not a palindrome.

Note:
Have you consider that the string might be empty? This is a good question to ask during an interview.

For the purpose of this problem, we define empty string as valid palindrome.

SOLUTION:
    Straight-forward solution:
        - Convert to lower case, remove non-alpha numerics
        - compare forward and backward readings

    Amazing finding:
        (-3) / 2 IS different from -(3 / 2)
        Check it yourself
"""

import re

class Solution(object):
    def isPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """
        word = re.sub(r'\W', '', s).lower()
        n = len(word) / 2
        return word[:n] == word[-1:-n-1:-1]


import sys
from utils.templates import fail_string

def test():
    solution = Solution()
    for case, ans in [
        ('0P', False),
        ('', True),
        ('1', True),
        ("A man, a plan, a canal: Panama", True),
        ('race a car', False),
    ]:
        res = solution.isPalindrome(case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()