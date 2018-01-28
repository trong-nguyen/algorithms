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

SOLUTION:
    You have to learn how to count lexicographically. Basically the rules are:
    - From left to right
    - Empty < numerics: _ < 0 < 1 ... < 9
    - Counting depends on the maximum number of available digits. i.e. if in a count the max digits possible is 6,
    then 999999 will be the biggest. There are a total number of 11 groups:
        + Empty group
        + 9 numerical-prefixed groups:
            1 _
            1 x
            1 x x
            1 x x x
            1 x x x x
            1 x x x x x

            ...

            9 _
            9 x
            9 x x
            9 x x x
            9 x x x x
            9 x x x x x

        + After that, in each group, for ex. group 5 we would have 11 sub-groups including the first empty character group:
            5
              _ : first group is empty, which mean the number 5 itself

              0
              0 x
              0 x x
              0 x x x
              0 x x x x

            ...

              9
              9 x
              9 x x
              9 x x x
              9 x x x x

        + Successively:
            5
              5
                _ : empty

                0
                0 x
                0 x x
                0 x x x

            ...

                9
                9 x
                9 x x
                9 x x x

        + The formula is, except for the first digit, where the empty group and 0-prefixed group is excluded,
        the number of items in a group would be: sum(1 + 10^1 + 10^2 + ... + 10^(d-1)) where d is the max number of digits.
        It translates to
            d = 1: 1   items
            d = 2: 11  items
            d = 3: 111 items
            ...


    Problem framing: given n find k-th largest.
        - The digits are now capped by n not the total number of digits.
        - The counting then would be divided into 3 parts: let's take n=5437
            + First part: i from 1 to 4, max digits are 4
                i=[1:4]
                  _
                  x
                  x x
                  x x x

            + Second part: i is 5, but capped by 437, max digits are 4
                5 _
                  x
                  x x
                  x x x

            + Third part: i from 6 to 9, with max digits are 3
                i=[6:9]
                  _
                  x
                  x x

        - In order to know our k-th largest falls in which bracket (first to third), note that the size of:
            + First part
                n1 is [1:4] * subgroups with 3 digits max = 4 * 111 = 555 numbers
            + Third part
                n3 is [6:9] * subgroups with 2 digits max = 4 * 11 = 44 numbers
            + Second part
                n2 = n - n1 - n3 = 5437 - 555 - 44 = 4838

        - Then if:
                   k <= 555:    search in the first part
             555 < k <= 5393:   search in the second part
            5393 < k:           search in the third part

        - The search in the first and third parts are similar:
            + All digits are allowed so we search for every possible digit
            + find the prefix i-th bracket by dividing k for the number of items in each brackets (depending on max digits allowed)
            + entering the i-th bracket, the problem is recursive by modulo of k_new = k % bracket items, number of max digits reduced by 1
            + Note that for the full bracket searching there are a total number of 1 (empty-charactered group) + 10 (digit-led group)
            + So we have to subtract 1 item (the empty character group) before proceeding into one of the 10 sub-bracket group. E.g:
                We need to find the k=34 largest number in the 2 digit search (e.g n=99), is equivalent to finding the
                k = k-1 = 33-th largest item in the 10 sub group (from 0x to 9x), each have 11 elements.
                That number is 4 from
                    first digit:  (34-1) / 11 + 1 = 4 (plus 1 due to 1-indexed)
                    second digit: [(34-1) % 11] / 1 = '' (empty since k=0 means the first item in the subbracket which is empty)

                Similary the 35-th largest would be 40 and 36-th is 41



        - The second part is tricky since we are capped somewhere in the middle of the bracket by the value n. However:
            + The first prefix is known (e.g. 5 in n=5437, k=5112)
            + New n would be calculated by n_new = n - n1 - n3 as above
            + New k would be k_new = k - n1
            + Then we can proceed recursively with the subproblem find the k_new largest item in the n_new number capped by n
            + Note that now in the sub problem the first prefix can be both empty and 0 since it is actually the second prefix in the original problem


"""

DEBUG = False

from math import log

BRACKETS = [int('1' * i) for i in range(1, 10)]

def full_bracket(d, k):
    """
    base 0
    d digits includes the prefix
    """
    if DEBUG: print '\t digits {}, k {}'.format(d, k)
    if k == 0:
        return ''
    if d == 1:
        return str(k - 1)

    k -= 1 # the 1st empty digit

    a = k / BRACKETS[d - 1]
    b = k % BRACKETS[d - 1]

    prefix = str(a)
    if DEBUG: print '\t[{}] FB'.format(prefix)
    return str(a) + full_bracket(d - 1, b)

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


    if DEBUG:
        print 'Fractional range: [0 {} {} {}]'.format(lower_brackets, n - upper_brackets, n)
        print '\tk={}, n={}'.format(k, n)

    if k <= lower_brackets:
        p = (k - 1)
        prefix = str(p / lower_bracket + 1)
        if DEBUG: print '[{}] Which Lower'.format(prefix)
        return prefix + full_bracket(d - 1, p % lower_bracket)
    elif k > n - upper_brackets:
        p = k - (n - upper_brackets) - 1
        prefix = str(n_digits[0] + 1 + p / upper_bracket)
        if DEBUG: print '[{}] Which Higher'.format(prefix)
        return prefix + full_bracket(d - 2, p % upper_bracket)
    else:
        prefix = str(n_digits[0])
        if DEBUG: print '[{}] Which Mid'.format(prefix)
        return prefix + fractional_bracket(''.join(map(str, n_digits[1:])), k - lower_brackets - 1)

def fractional_bracket(lim, k):
    if k == 0:
        return ''

    n_digits = map(int, str(lim))
    d = len(n_digits)

    if d == 1:
        return str(k - 1)

    n = int(lim) + BRACKETS[max((d - 1), 0)]
    k -= 1

    lower_bracket = BRACKETS[max((d - 1), 0)]
    lower_brackets = lower_bracket * max(n_digits[0], 0) # base is 1 (the first round) it has no 0 layer

    upper_bracket = BRACKETS[max((d - 2), 0)]
    upper_brackets = upper_bracket * (9 - n_digits[0])

    if DEBUG:
        print 'Fractional range: [0 {} {} {}]'.format(lower_brackets, n - upper_brackets, n)
        print '\tk={}, lim={}'.format(k, lim)

    if k < lower_brackets:
        p = k
        prefix = str(p / lower_bracket)
        if DEBUG: print '[{}] Lower'.format(prefix)
        return prefix + full_bracket(d - 1, p % lower_bracket)
    elif k >= n - upper_brackets:
        p = k - (n - upper_brackets)
        prefix = str(n_digits[0] + 1 + p / upper_bracket)
        if DEBUG: print '[{}] Higher'.format(prefix)
        return prefix + full_bracket(d - 2, p % upper_bracket)
    else:
        prefix = str(n_digits[0])
        if DEBUG: print '[{}] Fractional'.format(prefix)
        return prefix + fractional_bracket(lim[1:], k - lower_brackets)


class Solution(object):
    def findKthNumber(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """
        return which_bracket(n, k)

import random
import sys
from utils.templates import fail_string

def brute_force(n, k):
    l = list(range(1, n+1))
    l = map('{{:<{}}}'.format(len(str(n))).format, l)
    l = sorted(l)
    return int(l[k - 1])

def brute_force_array(n):
    l = list(range(1, n+1))
    l = map('{{:<{}}}'.format(len(str(n))).format, l)
    l = sorted(l)
    return l

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

        print 'Test {}: n={:<8} k={:<8} ans={:<8} passed!'.format(c, case[0], case[1], ans)


def test3():
    solution = Solution()

    for c in range(1000):
        case = generate_random_nk(random.randint(1, 10**5 + 1))
        res = solution.findKthNumber(*case)
        ans = str(brute_force(*case))
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

        print 'Test {}: n={:<8} k={:<8} ans={:<8} passed!'.format(c, case[0], case[1], ans)


def test_exhausted():
    solution = Solution()

    n = 10 ** 5
    ans_array = brute_force_array(n)
    for k in range(1, n+1):
        res = solution.findKthNumber(n, k)
        ans = ans_array[k - 1].strip()
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=(n, k))
            sys.exit(status)

        print 'Test {}: n={:<8} k={:<8} ans={:<8} passed!'.format(k, n, k, ans)

def test():
    solution = Solution()
    for case, ans in [
        ([90, 34], True),
        ([1695, 474], True),
        ([141275, 45794], True),
        ([9999, 8000], True),
        ((247887, 168074), True),
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
        (generate_random_nk(1000000), True),

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
    test2()
    test3()
    test_exhausted()