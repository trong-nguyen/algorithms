#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given a string containing just the characters '(' and ')', find the length of the longest valid (well-formed) parentheses substring.

For "(()", the longest valid parentheses substring is "()", which has length = 2.

Another example is ")()())", where the longest valid parentheses substring is "()()", which has length = 4.
"""

import sys
from utils.templates import fail_string

# def valid_parentheses(s):

def longest_parentheses(s):
    stack = [-1]
    max_length = 0
    for i, c in enumerate(s):
        if c == '(':
            stack.append(i)
        elif not stack:
            stack.append(i)
        else:
            stack.pop()
            if stack:
                max_length = max(i-stack[-1], max_length)
            else:
                stack.append(i)
    return max_length



# def longest_parentheses(s):
#     def _longest_parentheses(s, opener):
#         max_count = 0
#         count = 0
#         bucket = 0
#         for i, c in enumerate(s):
#             if c == opener:
#                 bucket += 1
#             elif bucket > 0:
#                 bucket -= 1
#                 count += 1
#                 max_count = max(max_count, count)
#             else:
#                 count = 0
#             print bucket, count
#         return max_count * 2

#     print _longest_parentheses(s, '('), _longest_parentheses(s[::-1], ')')
#     return min(_longest_parentheses(s, '('), _longest_parentheses(s[::-1], ')'))


class Solution(object):
    def longestValidParentheses(self, s):
        """
        :type s: str
        :rtype: int
        """
        return longest_parentheses(s)



def test():
    for case, ans in [
        (['(()(()(()'], 2),
        (['(()'], 2),
        (["))))())()()(()"], 4),
        (["()(()"], 2),
        (["(()"], 2),
        ([')()())'], 4),
    ]:
        res = longest_parentheses(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()