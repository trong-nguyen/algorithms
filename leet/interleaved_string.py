#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given s1, s2, s3, find whether s3 is formed by the interleaving of s1 and s2.

For example,
Given:
s1 = "aabcc",
s2 = "dbbca",

When s3 = "aadbbcbcac", return true.
When s3 = "aadbbbaccc", return false.

SOLUTION:
    The problem is simpler than others in the amount of mental effort required to come up with a solution
    In few words, it is again, an algorithm with backtracking techniques to gain performance
    Backtracking here includes memoization.
    The traversal used here is greedy depth-first-search

    The problem can be better and more well defined by:
    - Given strings s1, s2, s3, find a way to combine s1 and s2 alternatively to come up with s3
    - Starting at the beginnings i from s1, j from s2, s3[i+j] would be either:
        + Taken from s1[i] if s1[i] = s3[i+j] and s2[j] != s1[i]
        + Or taken from s2[j] in a similar logic
        + There is a case where s1[i] = s2[j] and we cannot determine to take s3[i+j] from, so we do both
        and follow through till the end to see which one is unsucessful and take note (in the successfull case we immediately return)
        + And also there is a case where s3[i+j] is not equal to s1[i] nor s2[j], this is an unsuccessful case, take note
    - So basically we can think of the algorithm is a binary tree traversal, we either go to s1 or s2 and take note which one leads to dead end
    and dive deep till the end.

    - Another problem coming up is iteration vs recursion implementation. Usually recursion is more elegant but takes up the call stack quickly
    - Better to convert it to the iteration form, in this case using a stack to keep track of the current path and the diverged point to backtrack
    if the taken direction failed.
"""

def is_interleaved(s1, s2, s3):
    if len(s3) != len(s1) + len(s2):
        return False

    m, n = len(s1), len(s2)
    backtrack = [(0, 0)]
    explored = set()
    while backtrack:
        i, j = backtrack.pop()
        if (i, j) in explored:
            continue

        explored.add((i, j))

        k = i + j
        if i == m or j == n:
            if s2[j:] == s3[k:] or s1[i:] == s3[k:]:
                return True
            else:
                continue

        if s3[k] not in (s1[i], s2[j]):
            continue

        if s1[i] == s2[j]:
            backtrack += [(i+1, j), (i, j+1)]
            continue

        while i < m and j < n and s1[i] != s2[j]:
            if s3[i+j] == s1[i]:
                i += 1
            elif s3[i+j] == s2[j]:
                j += 1
            else:
                break

        backtrack.append((i, j))

    return False


class Solution(object):
    def isInterleave(self, s1, s2, s3):
        """
        :type s1: str
        :type s2: str
        :type s3: str
        :rtype: bool
        """
        return is_interleaved(s1, s2, s3)

import random
import sys
from utils.templates import fail_string

def test():
    solution = Solution()
    for case, ans in [
        (["bbbbbabbbbabaababaaaabbababbaaabbabbaaabaaaaababbbababbbbbabbbbababbabaabababbbaabababababbbaaababaa",
            "babaaaabbababbbabbbbaabaabbaabbbbaabaaabaababaaaabaaabbaaabaaaabaabaabbbbbbbbbbbabaaabbababbabbabaab",
            "babbbabbbaaabbababbbbababaabbabaabaaabbbbabbbaaabbbaaaaabbbbaabbaaabababbaaaaaabababbababaababbababbbababbbbaaaabaabbabbaaaaabbabbaaaabbbaabaaabaababaababbaaabbbbbabbbbaabbabaabbbbabaaabbababbabbabbab"
            ], False),

        (['ef', 'gh', 'ehgf'], False),
        (['', '', ''], True),
        (['', 'a', 'a'], True),
        (['a', '', 'a'], True),
        (['a', '', 'b'], False),
        (['xyz', '', 'xyz'], True),
        (['xyz', 'xyz', 'xyz'*2], True),
        (['xyz', 'xyz', 'xxyzyz'], True),
        (['xyaaaaaz', 'xaaaaayz', 'xxyaaaaazaaaaayz'], True),
        (['aabcc', 'dbbca', 'aadbbcbcac'], True),
        (['aabcc', 'dbbca', 'aadbbbaccc'], False),
        (['a'*100000, 'a'*100000, 'a'*200000], True),
        (['a'*100000, 'b'*100000, 'a'*100000 + 'b'*100000], True),
        (['a'*100000, 'b'*100000, ''.join(random.sample('a'*100000 + 'b'*100000, 200000))], True),
    ]:
        res = solution.isInterleave(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()