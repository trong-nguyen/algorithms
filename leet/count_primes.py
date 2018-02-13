#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

def mark_primes(lim, is_prime):
    for i in range(min(2, lim)):
        is_prime[i] = False

    for i in range(2, lim):
        if not is_prime[i]:
            continue

        for j in range(i * i, lim, i):
            is_prime[j] = False

    # print is_prime
    return is_prime

def is_a_prime(x):
    if x < 2:
        return False

    for i in range(2, x):
        if i * i > x:
            break

        if x % i == 0:
            return False

    return True

class Solution(object):
    def countPrimes(self, n):
        """
        :type n: int
        :rtype: int
        """
        is_prime = [True] * n
        for i in range(min(2, n)):
            is_prime[i] = False

        for i in range(2, n):
            if not is_prime[i]:
                continue

            for j in range(i * i, n, i):
                is_prime[j] = False

        count = 0
        for i in range(2, n):
            if is_prime[i]:
                count += 1

        return count


import sys
from utils.templates import fail_string

def unit_test():
    for x, ans in [
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (5, True),
        (10, False),
        (137, True),
    ]:
        res = is_a_prime(x)
        assert res == ans, '{} is {} a prime'.format(x, 'not' if ans == False else '')

def test():
    solution = Solution()
    for case in [100, 1000, 10000]:
        print case
        res = solution.countPrimes(case)
        ans = len(filter(is_a_prime, range(case)))
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()
    unit_test()