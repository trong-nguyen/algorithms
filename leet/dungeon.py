#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The demons had captured the princess (P) and imprisoned her in the bottom-right corner of a dungeon. The dungeon consists of M x N rooms laid out in a 2D grid. Our valiant knight (K) was initially positioned in the top-left room and must fight his way through the dungeon to rescue the princess.

The knight has an initial health point represented by a positive integer. If at any point his health point drops to 0 or below, he dies immediately.

Some of the rooms are guarded by demons, so the knight loses health (negative integers) upon entering these rooms; other rooms are either empty (0's) or contain magic orbs that increase the knight's health (positive integers).

In order to reach the princess as quickly as possible, the knight decides to move only rightward or downward in each step.


Write a function to determine the knight's minimum initial health so that he is able to rescue the princess.

For example, given the dungeon below, the initial health of the knight must be at least 7 if he follows the optimal path RIGHT-> RIGHT -> DOWN -> DOWN.

-2 (K)  -3  3
-5  -10 1
10  30  -5 (P)

Notes:

The knight's health has no upper bound.
Any room can contain threats or power-ups, even the first room the knight enters and the bottom-right room where the princess is imprisoned.

SOLUTION:
    Dynamic Programing problem
    Iterating bottom up, where we know for sure what the result is
    Each cell can be reached from either top or left cell.
    To sustain, the knight must have the health level larger than
    the value in the destination cell, plus the one where the knight is currently at
    basically:
        H[i, j] = max(min(H[i+1, j], H[i, j+1]) - F[i, j], 1)
        H[n, n] = max(1 - F[n, n], 1)
"""

def hp(dungeon):
    def maxmin(right_value, bottom_value, cell_value):
        return max(min(right_value, bottom_value) - cell_value, 1)

    rows = len(dungeon)
    cols = len(dungeon[0])

    if rows == 0 or cols == 0:
        return 1

    # special cases when matrix becomes 1 dimensional
    if cols == 1:
        # transform to rows
        dungeon_1d = [row[0] for row in dungeon]
    elif rows == 1:
        dungeon_1d = dungeon[0]
    if rows == 1 or cols == 1:
        corner = max(1-dungeon_1d[-1], 1)
        h = corner
        for i in range(len(dungeon_1d)-2, -1, -1):
            h = max(h - dungeon_1d[i], 1)

        return h


    # boundary cells
    corner = max(1-dungeon[rows-1][cols-1], 1)
    column_boundary = [corner]
    row_boundary = [corner]
    for i in range(rows-2, -1, -1):
        h = max(column_boundary[0] - dungeon[i][cols-1], 1)
        column_boundary.insert(0, h)

    for i in range(cols-2, -1, -1):
        h = max(row_boundary[0] - dungeon[rows-1][i], 1)
        row_boundary.insert(0, h)

    # internal cells
    for k in range(min(rows, cols)-1):
        # workings strip by strip from bottom right up
        rowi = rows-k-2
        coli = cols-k-2
        corner = maxmin(row_boundary[-2], column_boundary[-2], dungeon[rowi][coli])

        # push the common cell (corner) to the strip
        new_column_boundary = [corner]
        new_row_boundary = [corner]

        # then for each vertical and horizontal strip
        # sequentially compute the value based on computed data from previous iteration
        for i in range(rowi-1, -1, -1):
            h = maxmin(column_boundary[i], new_column_boundary[0], dungeon[i][coli])
            new_column_boundary.insert(0, h)

        for i in range(coli-1, -1, -1):
            h = maxmin(row_boundary[i], new_row_boundary[0], dungeon[rowi][i])
            new_row_boundary.insert(0, h)

        column_boundary = new_column_boundary
        row_boundary = new_row_boundary

    if cols > rows:
        return row_boundary[0]
    elif cols < rows:
        return column_boundary[0]
    else:
        return min(row_boundary[0], column_boundary[0])

import sys
from utils.templates import fail_string

def test():
    for case, ans in [
        ([[1,-4,5,-99],[2,-2,-2,-1]], 3),

        ([[1,2,1],[-2,-3,-3],[3,2,-2]], 1),

        ([[3,-20,30],[-3,4,0]], 1),

        ([[-1, 1], [1, 2]], 2),

        ([[0,-3],[-10,0]], 4),

        ([
            [-2, -3, 3],
            [-5, -10, 1],
            [10, 30, -5],
        ], 7),

        ([[]], 1),


        ([[2],[1]], 1),

        ([[-3,5]], 4),
    ]:
        res = hp(case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()