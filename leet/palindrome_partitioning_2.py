#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given a string s, partition s such that every substring of the partition is a palindrome.

Return the minimum cuts needed for a palindrome partitioning of s.

For example, given s = "aab",
Return 1 since the palindrome partitioning ["aa","b"] could be produced using 1 cut.


"""
PCUTOFF = 5

def find_all_palindromes(s):
    """
    Return a set of all palindromes that has length >= cutoff
    """

    kmax = len(s)

    palindromes = {}
    for k in range(PCUTOFF, kmax + 1): # to capture kmax
        for i in range(kmax - k + 1): # similarly
            j = i + k
            if s[i] != s[j-1]:
                continue

            yes = False
            if k < PCUTOFF + 2 and _is_palindrome(s, i+1, j-1):
                yes = True
            elif i+1 in palindromes and j-1 in palindromes[i+1]:
                yes = True

            if yes:
                palindromes[i] = palindromes.get(i, set())
                palindromes[i].add(j)

    return palindromes

def _is_palindrome(s, i, j):
    d_ij = j - i
    if d_ij < 2:
        return True
    elif s[i] != s[j-1]:
        return False
    elif d_ij < 4:
        return True
    else:
        return _is_palindrome(s, i+1, j-1)

def is_palindrome(s, i, j, lookup):
    if j - i < PCUTOFF:
        return _is_palindrome(s, i, j)
    else:
        return i in lookup and j in lookup[i]

def cut(s, i, j, palindromes, mem):
    if j < i + 2:
        return 0
    elif (i, j) in mem:
        return mem[(i, j)]
    elif is_palindrome(s, i, j, palindromes):
        cost = 0
    else:
        cost = j - i - 1
        for k in range(i+1, j):
            if is_palindrome(s, i, k, palindromes):
                cost = min(cost, cut(s, k, j, palindromes, mem) + 1)



    mem[(i, j)] = cost

    return cost

def min_cut(s):
    palindromes = find_all_palindromes(s)
    mem = {}

    # print [s[i:j] for i, j in palindromes]
    # return 1
    # print palindromes
    # ps =
    return cut(s, 0, len(s), palindromes, mem)

class Solution(object):
    def minCut(self, s):
        """
        :type s: str
        :rtype: int
        """
        return min_cut(s)

import random
import sys
from utils.templates import fail_string

def test():
    for case, ans in [
        (["apjesgpsxoeiokmqmfgvjslcjukbqxpsobyhjpbgdfruqdkeiszrlmtwgfxyfostpqczidfljwfbbrflkgdvtytbgqalguewnhvvmcgxboycffopmtmhtfizxkmeftcucxpobxmelmjtuzigsxnncxpaibgpuijwhankxbplpyejxmrrjgeoevqozwdtgospohznkoyzocjlracchjqnggbfeebmuvbicbvmpuleywrpzwsihivnrwtxcukwplgtobhgxukwrdlszfaiqxwjvrgxnsveedxseeyeykarqnjrtlaliyudpacctzizcftjlunlgnfwcqqxcqikocqffsjyurzwysfjmswvhbrmshjuzsgpwyubtfbnwajuvrfhlccvfwhxfqthkcwhatktymgxostjlztwdxritygbrbibdgkezvzajizxasjnrcjwzdfvdnwwqeyumkamhzoqhnqjfzwzbixclcxqrtniznemxeahfozp"], 452),
        (["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"], 1),
        (['ab'], 1),
        ([''], 0),
        (['aab'], 1),
        (['abcdeffedcbaabcdeffedcbbabcdeffedcbaabcdeffedcbeabcdeffedcbaabcdeffedcbbabcdeffedcbaabcdeffedcbeabcdeffedcbaabcdeffedcbbabcdeffedcbaabcdeffedcbe'], 17),
        (['abcdeffedcbaabcdeffedcbbabcdeffedcbaabcdeffedcbe'], 5),
        (['abcdeffedcbaabcdeffedcbb'], 2),
        (['abcdeffedcba'], 0),
        (['aabbccbbdedeioie'], 3),
        ([''.join([random.choice('abcdefghijklmn') for i in range(100)])], True),
        ([''.join([random.choice('xyz') for i in range(100)])], True),
    ]:
        res = min_cut(*case)
        if ans is not True:
            try:
                assert res == ans
            except AssertionError as e:
                status = fail_string(res=res, ans=ans, case=case)
                sys.exit(status)

if __name__ == '__main__':
    test()