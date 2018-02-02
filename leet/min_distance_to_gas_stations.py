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

DEBUG = False

from math import ceil, floor
import heapq

# def min_distance(stations, k):
#     stations = sorted(stations)
#     distances = map(lambda x: x[0] - x[1], zip(stations[:-1], stations[1:]))
#     distances = distances[:max(len(distances), k)]

#     heapq.heapify(distances)


#     print distances
#     for i in range(k):
#         d = heapq.heappop(distances)
#         heapq.heappush(distances, d/2.0)
#         heapq.heappush(distances, d/2.0)

#         print distances

#     print distances
#     return -distances[0]

# def min_distance(stations, k):
#     stations = sorted(stations)
#     distances = map(lambda x: x[1] - x[0], zip(stations[:-1], stations[1:]))
#     distances = distances[:max(len(distances), k)]
#     distances = sorted(distances, reverse=True)

#     n = len(distances)

#     distance_sum = 0
#     n_star = 0
#     while n_star < n:
#         i = n_star
#         n_star += 1
#         distance_sum += distances[i]
#         if distance_sum / distances[i] > k:
#             break

#     while n_star > 0:
#         # shifting back untill a reasonable small distance is found
#         d_star = distances[n_star - 1]
#         ds = [floor(1. * distances[i] / d_star)  for i in range(n_star)]
#         reduction_basis = sum(ds)
#         if reduction_basis - n_star < k:
#             # k cuts are sufficient to make minmax at least as small as d[n_star - 1]
#             break
#         else:
#             n_star -= 1

#     if n_star < 1:
#         return distances[0]

#     reduction_basis = int(reduction_basis)

#     budget = k - reduction_basis + n_star

#     d_base = [(-d / d_round, d, d_round) for d, d_round in zip(distances, ds)]
#     heapq.heapify(d_base)
#     # print budget
#     print d_base
#     while budget > 0 and d_base:
#         _, d, d_round = heapq.heappop(d_base)
#         d_round += 1
#         new_d = (-d / d_round, d, d_round)
#         heapq.heappush(d_base, new_d)
#         budget -= 1

#         print d_base

    # return -d_base[0][0]



# def min_distance(stations, k):
#     stations = sorted(stations)
#     distances = map(lambda x: 1. * x[1] - x[0], zip(stations[:-1], stations[1:]))
#     # distances = distances[:max(len(distances), k)]
#     distances = sorted(distances, reverse=True)

#     # finding lower and upper bound
#     n = len(distances)

#     distance_sum = 0
#     range_start = 0
#     range_end = 0
#     for i in range(n):
#         distance_sum += distances[i]
#         k_accurate = 1. * distance_sum / distances[i] - (i + 1)
#         lower_bound = max(i, ceil(k_accurate) + 1)
#         upper_bound = k_accurate + i

#         if k >= lower_bound:
#             range_start = i
#             range_end = max(range_end, i + 1)
#         else:
#             break

#         if k >= upper_bound:
#             range_end = max(range_end, i + 1)

#         # if DEBUG: print '\tlower [{:.01f}], upper [{:.01f}]'.format(lower_bound, upper_bound)

#     # if DEBUG: print distances
#     # if DEBUG: print range_start, range_end

#     while range_start > 0:
#         ds = [max(distances[j] / distances[range_start], 2.) for j in range(range_start+1)]

#         # print [d - 1 for d in ds]
#         fl = sum([floor(d - 1) for d in ds])
#         # ce = sum([ceil(d - 1) for d in ds])
#         # av = sum([d - 1 for d in ds])
#         # print 'k={}, n={}, range_start={}'.format(k, n, range_start)
#         # print '\tfloor:', fl
#         # print '\taverg:', av
#         # print '\tceil: ', ce
#         if fl <= k:
#             break
#         range_start -= max(int(ceil(0.05 * (fl - k))), 1)

#     original_range_start = range_start
#     while range_start < n - 1:
#         ds = [max(distances[j] / distances[range_start+1], 2.) for j in range(range_start+1+1)]

#         # print [d - 1 for d in ds]
#         fl = sum([floor(d - 1) for d in ds])
#         # ce = sum([ceil(d - 1) for d in ds])
#         # av = sum([d - 1 for d in ds])
#         # print 'k={}, n={}, range_start={}'.format(k, n, range_start+1)
#         # print '\tfloor:', fl
#         # print '\taverg:', av
#         # print '\tceil: ', ce
#         if fl > k:
#             break
#         range_start += 1 # int(max(ceil(0.2 * (fl - k)), 1))

#     print 'Original {}, adjusted {}'.format(original_range_start, range_start)

def min_distance(stations, k):
    stations = sorted(stations)
    distances = map(lambda x: 1. * x[1] - x[0], zip(stations[:-1], stations[1:]))
    # distances = distances[:max(len(distances), k)]
    distances = sorted(distances, reverse=True)

    # finding lower and upper bound
    n = len(distances)

    distance_sum = 0
    np = 0
    for i in range(n):
        distance_sum += distances[i]
        if distance_sum / (k + 1) > distances[i]:
            break

        np = i + 1

    # min way first
    dmin = distance_sum / distances[np - 1]
    dm = [max(floor(distances[i] / dmin), 2) for i in range(np)]
    budget = k - (sum(dm) - np)
    print 'budget {}, np {}, parts {}, k {}, n {}'.format(budget, np, sum(dm) - np, k, n)

    # while np < n:
    #     dm = sum(distances[:np]) / (k + 1)
    #     d_min = [d / dm for d in distances[:np]]
    #     minimal_parts = map(floor, d_min)
    #     budget = k - (sum(minimal_parts) - np)

    #     if budget < 0:
    #         break

    #     print dm, budget, k, sum(minimal_parts), np

    #     np += 1





class Solution(object):
    def minmaxGasDist(self, stations, K):
        """
        :type stations: List[int]
        :type K: int
        :rtype: float
        """
        return min_distance(stations, K)


import random
import sys
from utils.templates import fail_string

def test():
    solution = Solution()
    for case, ans in [
        ([random.sample(range(1000000), 10), 100000], 1),
        ([random.sample(range(1000000), 2000), 15000], 1),
        ([[10,19,25,27,56,63,70,87,96,97], 3], 9.666666667),
        ([random.sample(range(1000000), 10), 10], 1),
        ([[2,10,29,35,52,54,57,62,67,95], 20], 3.8),
        ([[0, 0.1, 1.1, 3.1, 6.1], 3], 1),
        ([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 9], 0.5),
    ]:
        res = solution.minmaxGasDist(*case)
        # try:
        #     assert abs(res - ans) < 1e-6
        # except AssertionError as e:
        #     status = fail_string(res=res, ans=ans, case=case)
        #     sys.exit(status)

if __name__ == '__main__':
    test()