import numpy as np
np.seterr(divide='ignore') # suppress div 0 warnings
'''
find the maximum points pass through a line

Algorithm: basically we establish a polar coordinate with origin
situated at each point and find colinear points by detecting identical
theta coordinate.

for each point:
    for other points:
        compute dx, dy
        assign to hashmap according to dx/dy
            values either inf or dx/dy
        num of max colinear points = n - (hashmap size) + 1
'''

class Solution(object):
    def maxPoints(self, points):
        """
        :type points: List[Point]
        :rtype: int
        """

class Point(object):
    def __init__(self, a=0, b=0):
        self.x = a
        self.y = b

def colinear(points):
    n = len(points)

    # the f16 numpy data type is important to pass tricky test
    # for detecting slightly different, almost co-linear points
    x = np.array([p.x for p in points], dtype='f16')
    y = np.array([p.y for p in points], dtype='f16')

    max_size = 0

    for p in points:
        dx = x - p.x
        dy = y - p.y

        slopes = dy/dx

        # those that overlap with the origin will have 'nan' value
        aims = filter(lambda v: not np.isnan(v), slopes)
        num_origins = n - len(aims)

        overlapping_map = {}
        for i, k in enumerate(aims):
            overlapping_map[k] = overlapping_map.get(k, 0) + 1

        max_overlap = 0 if not overlapping_map else max(overlapping_map.values())

        colinear_points = num_origins + max_overlap

        max_size = max(max_size, colinear_points)

    return max_size

# Leetcode class for judging
class Solution(object):
    def maxPoints(self, points):
        """
        :type points: List[Point]
        :rtype: int
        """
        return colinear(points)

def test():
    arrays = [
        ([], 0),
        ([(1,2), (2,4), (0,0), (1,3), (2,6), (3,9)], 4),
        ([(0, 0), (0, 0), (0, 0), (0, 0)], 4),
        ([(0, 0), (0, 1), (1, 0), (1, 1), (1.5, 1.5)], 3),
        ([(0, 0), (0, 1), (0, 2), (0, 3)], 4),
        ([(0, 0), (1, 0), (2, 0), (3, 0)], 4),
        ([[0,0],[94911151,94911150],[94911152,94911151]], 2),
        ([[0,0],[1,1],[1,-1]], 2)
    ]
    for array, ans in arrays:
        points = [Point(a=a[0], b=a[1]) for a in array]

        res = colinear(points)
        print 'max colinear points is', res

        assert ans == res, 'failed test'

if __name__ == '__main__':
    test()


