#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given two arrays of length m and n with digits 0-9 representing two numbers. Create the maximum number of length k <= m + n from digits of the two. The relative order of the digits from the same array must be preserved. Return an array of the k digits. You should try to optimize your time and space complexity.

Example 1:
nums1 = [3, 4, 6, 5]
nums2 = [9, 1, 2, 5, 8, 3]
k = 5
return [9, 8, 6, 5, 3]

Example 2:
nums1 = [6, 7]
nums2 = [6, 0, 4]
k = 5
return [6, 7, 6, 0, 4]

Example 3:
nums1 = [3, 9]
nums2 = [8, 9]
k = 3
return [9, 8, 9]
"""

DEBUG = False
import heapq

def merge(nums1, nums2, i, j):
    # if (i, j) in mem:
    #     return mem[(i, j)]
    # print 'Merging', nums1[i:], nums2[j:]
    res = []
    m, n = len(nums1), len(nums2)
    while i < m or j < n:
        if i == m:
            res += nums2[j:]
            break
        elif j == n:
            res += nums1[i:]
            break
        elif nums1[i] > nums2[j]:
            res.append(nums1[i])
            i += 1
        elif nums1[i] < nums2[j]:
            res.append(nums2[j])
            j += 1
        else:
            r1 = [nums1[i]] + merge(nums1, nums2, i + 1, j)
            r2 = [nums2[j]] + merge(nums1, nums2, i, j + 1)
            res += max(r1, r2)
            break

    # mem[(i, j)] = res
    return res

def build_heap(nums, i, j):
    heap = [(-nums[i], i) for i in range(i, j)]
    heapq.heapify(heap)
    return heap

def compute_lim(m, n, j, k):
    # m len of first array
    # n len of second array
    # j current index of second array
    return min(m, m - (k - (n - j)) + 1)

def create_number(nums1, nums2, i, j, k, mem):
    if (i, j, k) in mem:
        return mem[(i, j, k)]

    if DEBUG: print nums1, nums2
    m, n = len(nums1), len(nums2)

    # to quit early
    if m + n - i - j == k:
        mem[(i, j, k)] = merge(nums1, nums2, i, j)
        return mem[(i, j, k)]

    number = []
    # add items to heaps

    ilim = compute_lim(m, n, j, k)
    heap1 = build_heap(nums1, i, ilim)

    jlim = compute_lim(n, m, i, k)
    heap2 = build_heap(nums2, j, jlim)
    while len(number) < k:
        if m + n - i - j == k - len(number):
            mem[(i, j, k)] = number + merge(nums1, nums2, i, j)
            return mem[(i, j, k)]

        if DEBUG: print heap_str(heap1), heap_str(heap2)
        if heap1 and heap2:
            a1, idx1 = heap1[0]
            a2, idx2 = heap2[0]

            di = idx1 - i
            dj = idx2 - j
            if a1 == a2:
                # if di < dj:
                #     heap = heap1
                #     working_array = 1
                # elif di > dj:
                #     heap = heap2
                #     working_array = 2
                # else:
                new_k = k - 1 - len(number)
                r1 = [-a1] + create_number(nums1, nums2, idx1 + 1, j, new_k, mem)
                r2 = [-a2] + create_number(nums1, nums2, i, idx2 + 1, new_k, mem)

                mem[(i, j, k)] = number + max(r1, r2)
                return mem[(i, j, k)]

            elif -a1 > -a2:
                heap = heap1
                working_array = 1
            else:
                heap = heap2
                working_array = 2
        else:
            if heap1:
                heap = heap1
                working_array = 1
            else:
                heap = heap2
                working_array = 2

        if DEBUG: print '\t', heap_str(heap)

        a, idx = heapq.heappop(heap)
        number.append(-a)
        while heap and heap[0][1] < idx:
            heapq.heappop(heap)

        if working_array == 1:
            di = idx - i
            i = idx + 1
            if ilim < m:
                heapq.heappush(heap, (-nums1[ilim], ilim))
                ilim += 1

            jlim = compute_lim(n, m, i, k - len(number))
            heap2 = build_heap(nums2, j, jlim)

        elif working_array == 2:
            dj = idx - j
            j = idx + 1
            if jlim < n:
                heapq.heappush(heap, (-nums2[jlim], jlim))
                jlim += 1


            ilim = compute_lim(m, n, j, k - len(number))
            heap1 = build_heap(nums1, i, ilim)

        if DEBUG: print '\t', heap_str(heap1), heap_str(heap2)
        if DEBUG: print '\t\t', number, '\n'

    mem[(i, j, k)] = number
    return number

def heap_str(heap):
    return [-v for v,_ in heap]

class Solution(object):
    def maxNumber(self, nums1, nums2, k):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type k: int
        :rtype: List[int]
        """
        mem = {}
        return create_number(nums1, nums2, 0, 0, k, mem)

import random
import sys
from utils.templates import fail_string, debug

def test():
    solution = Solution()
    for case, ans in [
        ([[9,5,6,2,4,3,6,2], [5,7,6,2,2,1,3,0,2,8,9,7,7,3,2,2,9,4,5,1], 28], [9,5,7,6,5,6,2,4,3,6,2,2,2,1,3,0,2,8,9,7,7,3,2,2,9,4,5,1]),
        ([[4,6,9,1,0,6,3,1,5,2,8,3,8,8,4,7,2,0,7,1,9,9,0,1,5,9,3,9,3,9,7,3,0,8,1,0,9,1,6,8,8,4,4,5,7,5,2,8,2,7,7,7,4,8,5,0,9,6,9,2],
            [9,9,4,5,1,2,0,9,3,4,6,3,0,9,2,8,8,2,4,8,6,5,4,4,2,9,5,0,7,3,7,5,9,6,6,8,8,0,2,4,2,2,1,6,6,5,3,6,2,9,6,4,5,9,7,8,0,7,2,3], 60],
            [9,9,9,9,9,9,9,9,9,9,9,9,9,8,8,6,8,8,4,4,5,7,5,2,8,2,7,7,7,4,8,5,0,9,6,9,2,0,2,4,2,2,1,6,6,5,3,6,2,9,6,4,5,9,7,8,0,7,2,3]),
        ([[8, 9], [3, 9], 3], [9, 8, 9]),
        ([[1,6,5,4,7,3,9,5,3,7,8,4,1,1,4], [4,3,1,3,5,9], 21], [4,3,1,6,5,4,7,3,9,5,3,7,8,4,1,3,5,9,1,1,4]),
        ([[8, 9, 3, 9, 8, 9, 3, 9], [3, 9, 8, 9, 3, 9, 8, 9], 9], [9, 9, 9, 9, 9, 9, 9, 8, 9]),
        ([[1, 1, 9], [1, 1, 9], 3], [9, 1, 9]),
        ([random.sample(range(100000), 100000), random.sample(range(100000), 100000), 20], True),
        # ([random.sample(range(100000), 100000), random.sample(range(100000), 100000), 100000], True),
        ([[1, 2, 9, 3], [1, 2, 9, 3], 2], [9, 9]),
        ([[1, 2, 9, 3], [], 2], [9, 3]),
        ([[], [1, 2, 9, 3], 2], [9, 3]),
        ([[3, 4, 6, 5], [9, 1, 2, 5, 8, 3], 5], [9, 8, 6, 5, 3]),
        ([[6, 7], [6, 0, 4], 5], [6, 7, 6, 0, 4]),
        ([[8, 8, 8], [8, 8, 8, 8], 7], [8, 8, 8, 8, 8, 8, 8]),
    ]:
        res = solution.maxNumber(*case)
        if ans is not True:
            try:
                assert res == ans
            except AssertionError as e:
                status = fail_string(res=res, ans=ans, case=case)
                sys.exit(status)

if __name__ == '__main__':
    test()