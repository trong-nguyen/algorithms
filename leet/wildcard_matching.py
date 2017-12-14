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

import re

def is_match(s, p):
    pattern = p
    pattern = pattern.replace('?', '.{1}')
    pattern = re.sub(r'\*{2,}', '*', pattern)
    pattern = re.sub(r'\?\*', '.+', pattern)
    pattern = pattern.replace('*', '.*?')
    pattern += '$'
    c = re.compile(pattern)
    print pattern
    return c.match(s) != None

class Solution(object):
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        return is_match(s, p)

import sys
from utils import fail_string

def test():
    obj = Solution()
    for case, ans in [
        (["aa","a"], False),
        (["aa","aa"], True),
        (["aaa","aa"], False),
        (["aa", "*"], True),
        (["aa", "a*"], True),
        (["ab", "?*"], True),
        (["aab", "c*a*b"], False),
        (["aaaabaaaabbbbaabbbaabbaababbabbaaaababaaabbbbbbaabbbabababbaaabaabaaaaaabbaabbbbaababbababaabbbaababbbba", "*****b*aba***babaa*bbaba***a*aaba*b*aa**a*b**ba***a*a*"], True),
        (["abbabaaabbabbaababbabbbbbabbbabbbabaaaaababababbbabababaabbababaabbbbbbaaaabababbbaabbbbaabbbbababababbaabbaababaabbbababababbbbaaabbbbbabaaaabbababbbbaababaabbababbbbbababbbabaaaaaaaabbbbbaabaaababaaaabb",
            "**aa*****ba*a*bb**aa*ab****a*aaaaaa***a*aaaa**bbabb*b*b**aaaaaaaaa*a********ba*bbb***a*ba*bb*bb**a*b*bb"], False)
    ]:
        print case
        res = obj.isMatch(*case)
        try:
            assert res == ans
        except AssertionError as e:
            sys.exit(fail_string(res=res, ans=ans, case=case))

if __name__ == '__main__':
    test()