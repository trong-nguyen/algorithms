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
    if d == 1:
        return str(k - 1)

    k -= 1 # the 1st empty digit

    a = k / BRACKETS[d - 1]
    b = k % BRACKETS[d - 1]

    return str(a) + full_bracket(d - 1, b)

def mix_bracket(d, k):
    """
    base 0
    d digits includes the prefix
    """
    print '\t digits {}, k {}'.format(d, k)
    if k == 0:
        return ''
    if d == 1:
        return str(k - 1)

    k -= 1 # the 1st empty digit

    bracket = 10 ** d + BRACKETS[d - 1]

    a = k / bracket
    b = k % bracket

    return str(a) + mix_bracket(d - 1, b)


def which_bracket(n, k):
    """
    Base 1
    """
    if n < 10:
        return str(k)

    n_digits = map(int, str(n))
    d = len(str(n))


    lower_bracket = BRACKETS[max((d - 1), 0)]
    lower_brackets = lower_bracket * max(n_digits[0] - 1, 0) # base is 1 (the first round) it has no 0 layer

    upper_bracket = BRACKETS[max((d - 2), 0)]
    upper_brackets = upper_bracket * (9 - n_digits[0])

    print lower_brackets, n - upper_brackets, n, 'n {}, k {}, d {}'.format(n, k, d)

    if k <= lower_brackets:
        p = (k - 1)
        prefix = str(p / lower_bracket + 1)
        return prefix + full_bracket(d - 1, p % lower_bracket)
    elif k > n - upper_brackets:
        p = k - (n - upper_brackets) - 1
        prefix = str(n_digits[0] + 1 + p / upper_bracket)
        return prefix + full_bracket(d - 2, p % upper_bracket)
    else:
        p = n - lower_brackets - upper_brackets - 1
        prefix = str(n_digits[0])
        return prefix + fractional_bracket(''.join(map(str, n_digits[1:])), k - lower_brackets - 1)
        # prefix = str(n_digits[0])
        # return prefix + full_bracket(d - 1, k - lower_brackets - 1)

def fractional_bracket(lim, k):
    if k == 0:
        return ''

    n_digits = map(int, str(lim))
    d = len(n_digits)

    if d == 1:
        return str(k - 1)

    n = int(lim) + BRACKETS[max((d - 1), 0)] - 1
    k -= 1

    lower_bracket = 10 ** (d - 1) + BRACKETS[max((d - 2), 0)]
    lower_brackets = lower_bracket * max(n_digits[0], 0) # base is 1 (the first round) it has no 0 layer

    upper_bracket = BRACKETS[max((d - 2), 0)]
    upper_brackets = upper_bracket * (9 - n_digits[0])

    print 'Range:', lower_bracket, upper_bracket
    print '\tn {}, k {}, d {}'.format(n, k, d)

    if k < lower_brackets:
        p = k
        prefix = str(p / lower_bracket)
        return prefix + mix_bracket(d - 1, p % lower_bracket)
    elif k >= n - upper_brackets:
        p = k - (n - upper_brackets)
        prefix = str(n_digits[0] + p / upper_bracket)
        return prefix + full_bracket(d - 2, p % upper_bracket)
    else:
        return str(n_digits[0]) + fractional_bracket(lim[1:], k - lower_brackets)




def k_lexico(n, k):
    if n < 9:
        return str(k)

    res = which_bracket(n, k)
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


def generate_random_nk(n):
    n = random.randint(1, n)
    k = random.randint(1, n)
    return n, k


def test2():
    solution = Solution()

    for c in range(100):
        case = generate_random_nk(random.randint(1, 10**6 + 1))
        res = solution.findKthNumber(*case)
        ans = str(brute_force(*case))

        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

        print 'Test {}: n={:<8}, k={:<8}, ans={:<8}, passed.'.format(c, case[0], case[1], ans)


def test():
    solution = Solution()
    for case, ans in [
        ([1695, 474], True),
        ([141275, 45794], True),
        ([9999, 8000], True),
        ([6716, 6355], True),
        ([852, 826], True),
        ([35, 15], True),
        ([10, 3], True),
        ([38, 25], True),
        ([35, 32], True),
        ([15, 4], True),
        ([2, 2], True),
        ([10, 3], True),
        ([1, 1], True),
        ([13, 2], True),
        ([349, 15], True),
        ([1000, 578], True),
        ([222, 222], True),

        ([100, 57], True),

        (generate_random_nk(100), True),
        (generate_random_nk(1000), True),
        (generate_random_nk(10000), True),
        (generate_random_nk(100000), True),

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
    # test2()