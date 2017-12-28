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

SOLUTION:
    This problem is a genius modification of the original problem where greedy approach will work.
    Though the solution to the original problem does not solve this problem correctly. Understanding it
    will help devise a solution to this problem.
    - Original problem: single thread (one picker at a time, one pass, etc.).
        At a certain time, one picker can only proceed right or down. Hence the DP form will be:
            DP[i,j] = F[i,j] + max(DP[i+1,j], DP[i, j+1])
            Proceed bottom up, the boundary condition will be the right and bottom edges.
            Solution is at DP[0, 0].
    - This problem: dual thread (2 pickers, or 2 passes, up and down).
        Now, at a certain time, we have 2 workers being somewhere on the diagonal line i+j = k
        where k ranges from 0 to 2n-2. The DP form will be:
            Basically that means for each row on the diagonal line i+j=k. Pick 2 points (n2 choices).
            (i1, j1), (i2, j2). The most cherries that these 2 workers can pick will be:
                * the cherries at those points F[i1, j1] + F[i2, j2] (minus 1 if i1=j1, i2=j2)
                * plus the most cherries 2 can pick in one of the scenarios:
                    + 1st worker moves right, 2nd moves right
                    + 1st worker moves right, 2nd moves down
                    + 1st worker moves down, 2nd moves right
                    + 1st worker moves down, 2nd moves down

            Programmatically:
            DP[(i1,j1), (i2,j2)] = Non-overlapped(F[i1,j1] + F[i2,j2]) + max(
                DP[(i1,j1+1), (i2+1,j2)],
                DP[(i1,j1+1), (i2,j2+1)],
                DP[(i1+1,j1), (i2+1,j2)],
                DP[(i1+1,j1), (i2,j2+1)],
            )
            Since for each diagonal levels the constraint i+j = k holds we can simplify the formula further:
            DP[i1,i2] = Non-overlapped(F[i1,j1] + F[i2,j2]) + max(
                DP'[i1,i2],
                DP'[i1,i2+1],
                DP'[i1+1,i2],
                DP'[i1+1,i2+1],
            )
            where DP' is the obtained solution at level k+1 (solved)

            O(n3) time, O(n2) space
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
    # dual = [possibilities]
    # k ranges from 0 to 2n-2 (total 2n-1 levels)
    # hence the second last level is 2n-3
    for k in range(2*n-3, -1, -1):
        new_possibilities = {}
        if k >= n:
            # bottom right triangle
            rows = (k-n+1, n)
            cols = (n-1, k-n, -1)
        else:
            # upper left triangle
            rows = (0, k+1)
            cols = (k, -1, -1)

        for r1, c1 in zip(range(*rows), range(*cols)):
            for r2, c2 in zip(range(r1, rows[-1]), range(c1, cols[-1], -1)):
                if matrix[r1][c1] == -1 or matrix[r2][c2] == -1:
                    new_possibilities[(r1, r2)] = -1
                    continue

                f = matrix[r1][c1]

                if r1 != r2:
                    f += matrix[r2][c2]

                fnb = -1

                for move in [
                    (r1, r2),
                    (r1, r2+1),
                    (r1+1, r2),
                    (r1+1, r2+1),
                ]:
                    # this will take care of edge cases
                    if move in possibilities:
                        fnb = max(fnb, possibilities[move])

                if fnb == -1:
                    # stuck no matter what
                    new_possibilities[(r1, r2)] = -1
                else:
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
    # greedy approach, is correct for some cases
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

def pick_2_cherries(field):
    # print 'Field\n', cherry_field_str(field)
    # field = [list(row) for row in field]
    cherries = build_dual_possibility_matrix(field)
    return 0 if cherries == -1 else cherries


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
        # res = pick_cherry(case) # single thread, wrong results
        res = pick_2_cherries(case) # dual thread, dual possibilities
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()