#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import sys
from utils import fail_string

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
    test()