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

import math
import heapq

def min_distance(stations, k):
    stations = sorted(stations)
    distances = map(lambda x: x[0] - x[1], zip(stations[:-1], stations[1:]))
    distances = distances[:max(len(distances), k)]

    heapq.heapify(distances)


    print distances
    for i in range(k):
        d = heapq.heappop(distances)
        heapq.heappush(distances, d/2.0)
        heapq.heappush(distances, d/2.0)

        print distances

    print distances
    return -distances[0]

def min_distance(stations, k):
    stations = sorted(stations)
    distances = map(lambda x: x[1] - x[0], zip(stations[:-1], stations[1:]))
    distances = distances[:max(len(distances), k)]
    distances = sorted(distances, reverse=True)

    n = len(distances)

    distance_sum = 0
    minmax_distance = 0

    print distances
    for i in range(n):
        if distances[i] < 1e-8:
            break

        distance_sum += distances[i]

        j_max = (k + i + 1.0) * distances[i] / distance_sum


        # print '\tj* {}, mmd {}'.format(j_max, minmax_distance)
        # if i < n - 1:
        #     j_max = min(j_max, math.ceil(distances[i] / distances[i+1]))

        print '\tj* {}, mmd {}'.format(j_max, minmax_distance)
        if j_max < 2:
            break

        minmax_distance = 1.0 * distances[i] / j_max

        # if i < n - 1:
        #     minmax_distance = max(minmax_distance, distances[i+1])

        print j_max, minmax_distance

    return minmax_distance


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
        ([[10,19,25,27,56,63,70,87,96,97], 3], 9.66667),
        ([[0, 0.1, 1.1, 3.1, 6.1], 3], 1),
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