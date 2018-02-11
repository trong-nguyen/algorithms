#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A move consists of taking a point (x, y) and transforming it to either (x, x+y) or (x+y, y).

Given a starting point (sx, sy) and a target point (tx, ty), return True if and only if a sequence of moves exists to transform the point (sx, sy) to (tx, ty). Otherwise, return False.

Examples:
Input: sx = 1, sy = 1, tx = 3, ty = 5
Output: True
Explanation:
One series of moves that transforms the starting point to the target is:
(1, 1) -> (1, 2)
(1, 2) -> (3, 2)
(3, 2) -> (3, 5)

Input: sx = 1, sy = 1, tx = 2, ty = 2
Output: False

Input: sx = 1, sy = 1, tx = 1, ty = 1
Output: True

Note:

sx, sy, tx, ty will all be integers in the range [1, 10^9].

SOLUTION:
    O(logn) time (successively reduced by divisions) and O(1) space

    Note that tx and ty can be expressed as:
        tx = sx + i1*y1 + i2*y2 + i3*y3 + ... + i*ty
        ty = sy + j1*x1 + j2*x2 + j3*x3 + ... + j*ty
    where:
        y1 = sy, y2 = y1 + i1*x1, y3 = y2 + i2*x2
        x1 = sx, x2 = x1 + i1*y1, x3 = x2 + i2*y2

    Essentialy y1, y2, y3 if are possible scenarios where at step i=1,2,3
    we advance along x, i.e. x changes

    For example if at step 1 (the first step) we decided to advance along x
    then x2 = sx + i1*y1 and y2 = y1 = sx
    or if we advanced along y then y2 = sy + j1*x1 and x2 = x1 = sx
    But only one of them can happen i.e.:
        tx = sx + i1*y1 + 0     + i3*y3 + ...
        ty = sy + 0     + j2*x2 + 0     + ...
    OR:
        tx = sx + 0     + i2*y2 + 0     + ...
        ty = sy + j1*x1 + 0     + j3*x3 + ...

    But which one will happen can be decided at step i by compare xi and yj
    if xi >= yj then probably we can only reach xi by using yj and vice versa
    if yj > xi then we reached yj by advancing along x in the previous step.

    Now working backward from tx=xn and ty=ym we successively deduce x(n-1) and y(m-1)
    by x(n-1) = (tx - sx) % ym + sx if x(n) >= ym.

    We stop when tx - sx < yj or ty - sy < xi since it signals that we could not reach
    xi or yj by using y(j) or xi in the previous step.

"""
class Solution(object):
    def reachingPoints(self, sx, sy, tx, ty):
        """
        :type sx: int
        :type sy: int
        :type tx: int
        :type ty: int
        :rtype: bool
        """
        while tx > sx or ty > sy:
            t, s, t_lower = (tx, sx, ty) if tx >= ty else (ty, sy, tx)

            d = t - s
            if d < t_lower:
                return False

            t = s + d % t_lower

            if tx >= ty:
                tx = t
            else:
                ty = t

        return tx == sx and ty == sy

import sys
from utils.templates import fail_string

def test():
    solution = Solution()
    for case, ans in [
        ([1, 1, 3, 5], True),
        ([1, 1, 2, 2], False),
        ([1, 1, 1, 1], True),
        ([1, 2, 39, 17], True),
    ]:
        res = solution.reachingPoints(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()