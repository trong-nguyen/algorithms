#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given integers n and k, find the lexicographically k-th smallest integer in the range from 1 to n.

Note: 1 ≤ k ≤ n ≤ 109.

Example:

Input:
n: 13   k: 2

Output:
10

Explanation:
The lexicographical order is [1, 10, 11, 12, 13, 2, 3, 4, 5, 6, 7, 8, 9], so the second smallest number is 10.
"""

from math import log

BRACKETS = [int('1' * i) for i in range(1, 10)]

def full_bracket(d, k):
    """
    base 0
    d digits includes the prefix
    """
    print '\t digits {}, k {}'.format(d, k)
    if k == 0:
        return ''
    elif d == 1:
        return str(k - 2)

    a = k / BRACKETS[d - 1]
    b = k % BRACKETS[d - 1]
    print '\t\t', a, b
    return str(a) + full_bracket(d - 1, b)

def which_bracket(n, k):
    """
    Base 1
    """
    if n < 10:
        return str(k)

    n_digits = map(int, str(n))
    d = len(str(n))

    B1 = BRACKETS[max((d - 1), 0)]
    B2 = BRACKETS[max((d - 2), 0)]

    lower_bracket = max(n_digits[0] - 1, 0)
    lower_brackets = lower_bracket * B1 # base is 1 (the first round) it has no 0 layer

    upper_bracket = 9 - n_digits[0]
    upper_brackets = upper_bracket * B2

    print lower_brackets, n - upper_brackets, n, 'n {}, k {}, d {}'.format(n, k, d)

    if k <= lower_brackets:
        p = (k - 1)
        prefix = str(p / lower_bracket)
        return prefix + full_bracket(d - 1, p % lower_bracket)
    elif k > n - upper_brackets:
        p = k - (n - upper_brackets) - 1
        prefix = str(n_digits[0] + 1 + p / upper_bracket)
        return prefix + full_bracket(d - 2, p % upper_bracket)
    else:
        p = n - lower_brackets - upper_brackets - 1
        return str(n_digits[0]) + fractional_bracket(p, k - lower_brackets - 1)

def fractional_bracket(n, k):
    if k == 0:
        return ''
    elif n < 11:
        return str(k - 2)

    n_digits = map(int, str(n))
    d = len(n_digits)

    B1 = BRACKETS[max((d - 1), 0)]
    B2 = BRACKETS[max((d - 2), 0)]

    lower_bracket = n_digits[0]
    lower_brackets = lower_bracket * B1 # base is 1 (the first round) it has no 0 layer

    upper_bracket = 9 - n_digits[0]
    upper_brackets = upper_bracket * B2

    print lower_brackets, n - upper_brackets, n, 'n {}, k {}, d {}'.format(n, k, d)

    if k < lower_brackets:
        p = k
        prefix = str(p / lower_bracket)
        return prefix + full_bracket(d - 1, p % lower_bracket)
    elif k >= n - upper_brackets:
        p = k - (n - upper_brackets)
        prefix = str(n_digits[0] + 1 + p / upper_bracket)
        return prefix + full_bracket(d - 2, p % upper_bracket)
    else:
        p = n - lower_brackets - upper_brackets
        return str(n_digits[0]) + fractional_bracket(p, k - lower_brackets)




def k_lexico(n, k):
    if n < 9:
        return str(k)

    res = which_bracket(n, k, 1)
    return res
    # return int(str(int(res[0]) + 1) + res[1:])



class Solution(object):
    def findKthNumber(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """
        return k_lexico(n, k)

import random
import sys
from utils.templates import fail_string

def brute_force(n, k):
    l = list(range(1, n+1))
    l = map('{{:<{}}}'.format(len(str(n))).format, l)
    l = sorted(l)
    return int(l[k - 1])

def test():
    def generate_random_nk(n):
        n = random.randint(1, n)
        k = random.randint(1, n)
        return n, k


    solution = Solution()
    for case, ans in [
        # ([10, 3], True),
        ([38, 25], True),
        (generate_random_nk(100), True),
        (generate_random_nk(1000), True),
        (generate_random_nk(10000), True),
        ([222, 222], True),
        ([100, 57], True),
        ([1000, 578], True),

        ([35, 32], True),
        ([35, 15], True),
        ([15, 4], True),
        ([2, 2], True),
        ([10, 3], True),
        ([1, 1], True),
        ([13, 2], True),

    ]:
        res = solution.findKthNumber(*case)
        if ans is True:
            ans = str(brute_force(*case))
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()