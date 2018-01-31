#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
On a horizontal number line, we have gas stations at positions stations[0], stations[1], ..., stations[N-1], where N = stations.length.

Now, we add K more gas stations so that D, the maximum distance between adjacent gas stations, is minimized.

Return the smallest possible value of D.

Example:

Input: stations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], K = 9
Output: 0.500000
Note:

stations.length will be an integer in range [10, 2000].
stations[i] will be an integer in range [0, 10^8].
K will be an integer in range [1, 10^6].
Answers within 10^-6 of the true value will be accepted as correct.
"""

import heapq

def min_distance(stations, k):
    stations = sorted(stations)
    distances = map(lambda x: x[0] - x[1], zip(stations[:-1], stations[1:]))

    heapq.heapify(distances)

    for i in range(k):
        d = heapq.heappop(distances)
        heapq.heappush(distances, d/2.0)
        heapq.heappush(distances, d/2.0)

    print distances
    return -distances[0]


class Solution(object):
    def minmaxGasDist(self, stations, K):
        """
        :type stations: List[int]
        :type K: int
        :rtype: float
        """
        return min_distance(stations, K)


import sys
from utils.templates import fail_string

def test():
    solution = Solution()
    for case, ans in [
        ([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 9], 0.5),
    ]:
        res = solution.minmaxGasDist(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()