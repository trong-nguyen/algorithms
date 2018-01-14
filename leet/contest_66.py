#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""



import sys
from utils.templates import fail_string

def partition_labels(s):
    d = {}
    for i, c in enumerate(s):
        if c not in d:
            d[c] = [i, i+1]
        else:
            d[c][1] = i+1
    # return d

    segments = sorted(d.values())

    partitions = [segments[0]]
    for i, j in segments[1:]:
        end = partitions[-1][1]
        if i >= end:
            partitions.append([i, j])
        elif j > end:
            partitions[-1][1] = j

    return map(lambda x: x[1]-x[0], partitions)

class Solution_1(object):
    def partitionLabels(self, S):
        """
        :type S: str
        :rtype: List[int]
        """
        return partition_labels(S)


def set_bits(n):
    c = 0
    while n > 0:
        n = n & (n-1)
        c += 1

    return c

def is_prime(n, mem):
    if n <= 1:
        return False

    if n in mem:
        return mem[n]


    x = 2
    while x ** 2 <= n:
        if n % x == 0:
            mem[n] = False
            return False
        x += 1

    mem[n] = True
    return True

def count_prime_set_bits(L, R):
    count = 0
    mem = {}
    for x in range(L, R+1):
        if is_prime(set_bits(x), mem):
            count += 1

    return count

class Solution_2(object):
    def countPrimeSetBits(self, L, R):
        """
        :type L: int
        :type R: int
        :rtype: int
        """
        return count_prime_set_bits(L, R)


def test():
    for case, ans in [
    ]:
        res = function(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    # test()
    print partition_labels('ababcbacadefegdehijhklij')
    print partition_labels('aa')
