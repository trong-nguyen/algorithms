#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import sys
from utils.templates import fail_string

def test():
    solution = Solution()
    for case, ans in [
    ]:
        res = solution.solve(*case)
        if ans is True:
            # we just want to test the algorithm on random inputs
            print res
            continue

        if ans is None:
            # we have a bruteforce algorithm to test against
            ans = bruteforce
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()