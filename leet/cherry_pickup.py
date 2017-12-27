#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
In a N x N grid representing a field of cherries, each cell is one of three possible integers.

0 means the cell is empty, so you can pass through;
1 means the cell contains a cherry, that you can pick up and pass through;
-1 means the cell contains a thorn that blocks your way.
Your task is to collect maximum number of cherries possible by following the rules below:

Starting at the position (0, 0) and reaching (N-1, N-1) by moving right or down through valid path cells (cells with value 0 or 1);
After reaching (N-1, N-1), returning to (0, 0) by moving left or up through valid path cells;
When passing through a path cell containing a cherry, you pick it up and the cell becomes an empty cell (0);
If there is no valid path between (0, 0) and (N-1, N-1), then no cherries can be collected.
Example 1:
Input: grid =
[[0, 1, -1],
 [1, 0, -1],
 [1, 1,  1]]
Output: 5
Explanation:
The player started at (0, 0) and went down, down, right right to reach (2, 2).
4 cherries were picked up during this single trip, and the matrix becomes [[0,1,-1],[0,0,-1],[0,0,0]].
Then, the player went left, up, up, left to return home, picking up one more cherry.
The total number of cherries picked up is 5, and this is the maximum possible.
Note:

grid is an N by N 2D array, with 1 <= N <= 50.
Each grid[i][j] is an integer in the set {-1, 0, 1}.
It is guaranteed that grid[0][0] and grid[N-1][N-1] are not -1.
"""

import numpy as np

def walk_down(matrix):
    n = len(matrix)

    i = 0
    j = 0
    path = [(i, j)]
    while (i < n or j < n):
        if i == n - 1:
            j += 1
        elif j == n - 1:
            i += 1
        elif matrix[i, j+1] >= matrix[i+1, j]:
            j += 1
        else:
            i += 1

        path.append((i, j))
        if i == j == n - 1:
            break

    return path




def build_potential_matrix(matrix):
    n = len(matrix)

    potential = np.matrix([np.zeros(n, dtype=int)] * n)
    # bcs
    potential[n-1, n-1] = matrix[n-1, n-1]
    potential[:, n-1] = matrix[:, n-1]
    for i in range(n-2, -1, -1):
        f = matrix[i, n-1]
        if f >= 0:
            potential[i, n-1] = potential[i+1, n-1] + matrix[i, n-1]
        else:
            potential[i, n-1] = -1

    for i in range(n-2, -1, -1):
        f = matrix[n-1, i]
        if f >= 0:
            potential[n-1, i] = potential[n-1, i+1] + matrix[n-1, i]
        else:
            potential[n-1, i] = -1

    # inner loop
    for k in range(n-2, -1, -1):
        for i in range(k, -1, -1):
            f = matrix[i, k]
            if f == -1:
                potential[i, k] = -1
            else:
                fr = potential[i, k+1]
                fd = potential[i+1, k]
                fnb = max(fr, fd)

                potential[i, k] = f + max(fr, fd)

        for i in range(k, -1, -1):
            f = matrix[k, i]
            if f == -1:
                potential[k, i] = -1
            else:
                fr = potential[k, i+1]
                fd = potential[k+1, i]
                potential[k, i] = f + max(fr, fd)

    return potential

def update_matrix(matrix, path):
    for i, j in path:
        matrix[i, j] = 0

def count_picked(matrix, path):
    cherries = 0
    for i, j in path:
        cherries += matrix[i, j]
    return cherries

def pick_cherry(field):
    #print field
    field = np.matrix(field)
    p = build_potential_matrix(field)
    #print p

    if p[0, 0] == -1:
        return 0

    path_1 = walk_down(p)
    cherries_down = count_picked(field, path_1)

    update_matrix(field, path_1)
    p = build_potential_matrix(field)
    path_2 = walk_down(p)
    cherries_up = count_picked(field, path_2)

    #print path_1
    #print path_2
    #print cherries_down + cherries_up
    return cherries_down + cherries_up

import sys
from utils.templates import fail_string
import random
def test():
    for case, ans in [
        ([[0, 1, -1],
         [1, 0, -1],
         [1, 1,  1]], 5),

        ([[1, 1, 1, 0],
         [1, 0, 0, 1],
         [0, 1, 0, 1],
         [1, 1, 1, 0]], 9),

        ([[1, 1, 1],
         [1, 0, 1],
         [1, 1, 0]], 7),

        ([[random.randint(-1, 1) for i in range(1000)] for j in range(1000)], 100),
    ]:
        res = pick_cherry(case)
        # try:
        #     assert res == ans
        # except AssertionError as e:
        #     status = fail_string(res=res, ans=ans, case=case)
        #     sys.exit(status)

if __name__ == '__main__':
    test()