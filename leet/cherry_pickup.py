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
        if i == j == n - 1:
            break

        if i == n - 1:
            j += 1
        elif j == n - 1:
            i += 1
        elif matrix[i][j+1] >= matrix[i+1][j]:
            j += 1
        else:
            i += 1

        path.append((i, j))

    return path

def build_dual_possibility_matrix(matrix):
    n = len(matrix)

    possibilities = {(n-1, n-1): matrix[n-1][n-1]}
    for k in range(n-2, -1, -1):
        new_possibilities = {}
        for r1 in range(k, n):
            c1 = k - r1
            for r2 in range(r1, n):
                c2 = k - r2

                if matrix[r1][c1] == -1 or matrix[r2][c2] == -1:
                    new_possibilities[(r1, r2)] = -1
                    continue

                f = matrix[r1][c1]

                if r1 != r2:
                    f += matrix[r2][c2]

                fnb = max([
                    possibilities[(r1, r2)],
                    possibilities[(r1, r2+1)],
                    possibilities[(r1+1, r2)],
                    possibilities[(r1+1, r2+1)],
                    ])

                if fnb == -1:
                    new_possibilities[(r1, r2)] = -1

                new_possibilities[(r1, r2)] = f + fnb

        possibilities = new_possibilities

    return possibilities[(0, 0)]





def build_potential_matrix(matrix):
    n = len(matrix)

    potential = [[0] * n for i in range(n)]
    # bcs
    potential[n-1][n-1] = matrix[n-1][n-1]
    # print 'Bc\n', matrix_str(potential)
    for i in range(n-2, -1, -1):
        f = matrix[i][n-1]
        if f >= 0:
            potential[i][n-1] = potential[i+1][n-1] + matrix[i][n-1]
        else:
            potential[i][n-1] = -1

    for i in range(n-2, -1, -1):
        f = matrix[n-1][i]
        if f >= 0:
            potential[n-1][i] = potential[n-1][i+1] + matrix[n-1][i]
        else:
            potential[n-1][i] = -1

    # print 'Bc\n', matrix_str(potential)
    # inner loop
    for k in range(n-2, -1, -1):
        for i in range(k, -1, -1):
            f = matrix[i][k]
            if f == -1:
                potential[i][k] = -1
            else:
                fr = potential[i][k+1]
                fd = potential[i+1][k]
                fnb = max(fr, fd)
                potential[i][k] = (f + fnb) if fnb != -1 else -1


        for i in range(k, -1, -1):
            f = matrix[k][i]
            if f == -1:
                potential[k][i] = -1
            else:
                fr = potential[k][i+1]
                fd = potential[k+1][i]
                fnb = max(fr, fd)
                potential[k][i] = (f + fnb) if fnb != -1 else -1

    return potential

def update_matrix(matrix, path):
    for i, j in path:
        matrix[i][j] = 0

def count_picked(matrix, path):
    cherries = 0
    for i, j in path:
        cherries += matrix[i][j]
    return cherries

def matrix_str(mat):
    return '\n'.join([' '.join(map('{:3}'.format, row)) for row in mat])

def cherry_field_str(field):
    def cherry_cell(cell):
        s = 'c' if cell == 1 else ['*', ''][cell==0]
        return '{:>3}'.format(s)
    return '\n'.join([' '.join(map(cherry_cell, row)) for row in field])

def pick_cherry(field):
    print 'Field\n', cherry_field_str(field)
    field = [list(row) for row in field]
    p = build_potential_matrix(field)
    print 'Potential\n', matrix_str(p)

    if p[0][0] in [-1, 0]:
        return 0

    path_1 = walk_down(p)
    cherries_down = count_picked(field, path_1)

    update_matrix(field, path_1)
    print 'Field 2\n', cherry_field_str(field)
    p = build_potential_matrix(field)
    print 'Potential 2\n', matrix_str(p)
    path_2 = walk_down(p)
    cherries_up = count_picked(field, path_2)

    print path_1
    print path_2
    print cherries_down + cherries_up
    return cherries_down + cherries_up

import sys
from utils.templates import fail_string
import random
def test():
    for case, ans in [
        ([[1,1,1,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,1],[1,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,1,1,1]], 15),
        ([[0, 0], [0, 0]], 0),
        ([[0]], 0),
        ([[1,1,-1],[1,-1,1],[-1,1,1]], 0),


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

        # ([[random.randint(-1, 1) for i in range(100)] for j in range(100)], 100),
    ]:
        res = pick_cherry(case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()