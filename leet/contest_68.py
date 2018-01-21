#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""
def traverse_diagonally(a, i, j, m, n):
    x = a[i][j]
    for i, j in zip(range(i, m), range(j, n)):
        if a[i][j] != x:
            return False

    return True

def is_toeplitz(a):
    m = len(a)
    n = len(a[0])

    for i in range(m):
        j = 0
        if not traverse_diagonally(a, i, j, m, n):
            return False

    for j in range(1, n):
        i = 0
        if not traverse_diagonally(a, i, j, m, n):
            return False

    return True

def max_chunk(array):
    n = 0
    a0 = -1
    m = -1
    chunk = []
    for a in array:
        m = max(a, m)
        chunk.append(a)
        if len(chunk) == m - a0:
            n += 1
            chunk = []
            a0 = m
        # print a, chunk, m - a0
    return n

import heapq
def reorganize_string(s):
    d = {}
    for c in s:
        d[c] = d.get(c, 0) + 1

    items = [(-v, k) for k,v in d.items()]
    heap = heapq.heapify(items)

    new_s = ''
    buff = heapq.heappop(items)
    while items:
        count, c = buff
        new_s += c
        if -count > 1:
            if not items:
                return ''
            tmp = heapq.heappop(items)
            heapq.heappush(items, (count+1, c))
            buff = tmp
        else:
            buff = heapq.heappop(items)

        if not items:
            count, c = buff
            if -count > 1:
                return ''
            else:
                new_s += c

    return new_s

def max_chunk_2(array):
    n = 0
    a0 = min(array) - 1
    m = a0
    chunk = []
    for a in array:
        print a, chunk, m - a0
        if a == m:
            n += 1
            chunk = []
            continue

        m = max(a, m)
        chunk.append(a)
        if len(chunk) == m - a0:
            n += 1
            chunk = []
            a0 = m
    if n == 0:
        return 1
    else:
        return n

class Solution(object):
    def reorganizeString(self, s):
        """
        :type S: str
        :rtype: str
        """
        return reorganize_string(s)

# class Solution(object):
#     def maxChunksToSorted(self, arr):
#         """
#         :type arr: List[int]
#         :rtype: int
#         """
#         return max_chunk(arr)


# class Solution(object):
#     def isToeplitzMatrix(self, matrix):
#         """
#         :type matrix: List[List[int]]
#         :rtype: bool
#         """
#         return is_toeplitz(matrix)

def test():
    arr = [1,1,0,0,1]
    assert max_chunk_2(arr) == 2, max_chunk_2(arr)

    arr = [2,1,3,4,4]
    assert max_chunk_2(arr) == 4, max_chunk_2(arr)


    s = "aab"
    print reorganize_string(s)

    s = "aaab"
    print reorganize_string(s)

    s = "bcaaa"
    print reorganize_string(s)

    arr = [4,3,2,1,0]
    assert max_chunk(arr) == 1, max_chunk(arr)

    arr = [1,0,2,3,4]
    assert max_chunk(arr) == 4, max_chunk(arr)

    a = [[1,2,3,4],[5,1,2,3],[9,5,1,2]]
    assert is_toeplitz(a) == True

    a = [[1,2],[2,2]]
    assert is_toeplitz(a) == False

if __name__ == '__main__':
    test()
