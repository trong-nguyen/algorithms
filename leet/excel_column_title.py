#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""
import bisect

ALPHABETS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
BASE = 26
BASE_26 = [1,
    27,
    703,
    18279,
    475255,
    12356631,
    321272407,
    8353082583,
    217180147159,
    5646683826135,
    146813779479511,
    3817158266467287,
    99246114928149463,
    2580398988131886039,
    67090373691429037015L,
    1744349715977154962391L,
    45353092615406029022167L,
    1179180408000556754576343L,
    30658690608014475618984919L,
    797125955808376366093607895L
]

def generate_counting_sequence(n, base):
    """
    Generate a convenient range look up
    ex:
        count = [r1, r2, r3, ...]
        where ri is the starting count when x has i digits
        i.e:
        when i has 2 digits
        r2 = 27 is when we start counting, which is at AA
    """
    count = [1]
    for i in range(1, n):
        count.append(count[-1] + base ** i)

    return count

class Solution(object):
    def convertToTitle(self, n):
        """
        :type n: int
        :rtype: str
        """
        assert n < BASE_26[-1]

        # this returns index i where n >= BASE_26[i-1]
        # i is actually the upper bound non inclusive ")"
        # hence number of digits is indeed i
        digits = bisect.bisect(BASE_26, n)
        n -= BASE_26[digits]

        s = ''
        for digit in range(digits - 1, -1, -1):
            units = BASE ** digit
            d = n / units
            s += ALPHABETS[d]
            n %= units

        return s


import random
import sys
from utils.templates import fail_string

def test():
    solution = Solution()
    for case, ans in [
        (1, 'A'),
        (3, 'C'),
        (26, 'Z'),
        (27, 'AA'),
        (28, 'AB'),
        (12356630, 'ZZZZZ'),
        (5646683826134, 'ZZZZZZZZZ'),
        (random.randint(1, BASE_26[-1]), ''),
    ]:
        res = solution.convertToTitle(case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()