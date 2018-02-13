#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Count the number of prime numbers less than a non-negative number, n.

SOLUTION:
    Consider global solution:
    - The algorithm scans for all non-prime numbers up to a limit
    - Instead of local solution of checking if is prime for each number within a limit

    The method is "Sieve of Seratothenes".
    Assume every number up to n is a prime
    Looping O(n) and utilize the fact that
    - if i is not already a prime, its square plus an arbitrary sum i^2 + ki for k = 0 ...
    is not a prime (checked!)
    - for every i-th we already mark all of its multiples to not be prime
    - the remained number are primes
"""


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
        if n < 3:
            return 0

        if n == 3:
            return 1

        # the index manipulation n/2 - 1
        # means only working on odd numbers
        # from 3 5 7 ... n
        is_prime = [True] * (n / 2 - 1)
        for i in range(3, n, 2):
            if not is_prime[i / 2 - 1]:
                continue

            for j in range(i * i, n, i):
                if j % 2 == 1:
                    is_prime[j / 2 - 1] = False

        return 1 + is_prime.count(True) # number 2, we start count from 3


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