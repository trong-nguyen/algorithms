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
import heapq

def merge(nums1, nums2, i, j):
    res = []
    m, n = len(nums1), len(nums2)
    while i < m or j < n:
        if i == m:
            res += nums2[j:]
            break
        elif j == n:
            res += nums1[i:]
            break
        elif nums1[i] >= nums2[j]:
            res.append(nums1[i])
            i += 1
        else:
            res.append(nums2[j])
            j += 1

    return res

def create_number(nums1, nums2, k):
    print nums1, nums2
    m, n = len(nums1), len(nums2)
    i = 0
    j = 0

    # to quit early
    if m + n - i - j == k:
        return merge(nums1, nums2, i, j)

    heap1 = []
    heap2 = []
    number = []
    # add items to heaps
    ilim = min(m, m - (k - n) + 1)
    for ii in range(i, ilim):
        heapq.heappush(heap1, (-nums1[ii], ii))

    jlim = min(n, n - (k - m) + 1)
    for jj in range(j, jlim):
        heapq.heappush(heap2, (-nums2[jj], jj))
    while len(number) < k:
        if m + n - i - j == k - len(number):
            return number + merge(nums1, nums2, i, j)

        print heap1, heap2
        if heap1 and heap2:
            a1, idx1 = heap1[0]
            a2, idx2 = heap2[0]
            if a1 == a2:
                di = idx1 - i
                dj = idx2 - j

                if di <= dj:
                    heap = heap1
                    working_array = 1
                else:
                    heap = heap2
                    working_array = 2

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

        print '\t', heap

        a, idx = heapq.heappop(heap)
        number.append(-a)
        while heap and heap[0][1] < idx:
            heapq.heappop(heap)

        if working_array == 1:
            i = idx + 1
            if ilim < m:
                heapq.heappush(heap, (-nums1[ilim], ilim))
                ilim += 1
        elif working_array == 2:
            j = idx + 1
            if jlim < n:
                heapq.heappush(heap, (-nums2[jlim], jlim))
                jlim += 1

        print '\t\t', number, '\n'

    return number

import random
import sys
from utils.templates import fail_string

def test():
    for case, ans in [
        ([random.sample(range(8), 8), random.sample(range(8), 8), 8], 1),
        ([[1, 2, 9, 3], [1, 2, 9, 3], 2], [9, 9]),
        ([[1, 2, 9, 3], [], 2], [9, 3]),
        ([[], [1, 2, 9, 3], 2], [9, 3]),
        ([[3, 4, 6, 5], [9, 1, 2, 5, 8, 3], 5], [9, 8, 6, 5, 3]),
        ([[6, 7], [6, 0, 4], 5], [6, 7, 6, 0, 4]),
        ([[3, 9], [8, 9], 3], [9, 8, 9]),
        ([[8, 8, 8], [8, 8, 8, 8], 7], [8, 8, 8, 8, 8, 8, 8]),
    ]:
        res = create_number(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()