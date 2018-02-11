#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import math

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution_1(object):
    def minDiffInBST(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        min_val = float('inf')

        queue = [root]
        while queue:
            # print [n.val for n in queue]
            node = queue.pop(0)

            if node.left:
                min_val = min(abs(node.val - self.left_value(node)), min_val)
                queue.append(node.left)

            if node.right:
                min_val = min(abs(node.val - self.right_value(node)), min_val)
                queue.append(node.right)

            if min_val == 1:
                return min_val # since only identical values

        return min_val

    def left_value(self, node):
        pointer = node.left

        if not pointer:
            return float('inf')

        while pointer.right:
            pointer = pointer.right

        return pointer.val

    def right_value(self, node):
        pointer = node.right

        if not pointer:
            return float('inf')

        while pointer.left:
            pointer = pointer.left

        return pointer.val

import math
class Solution_2(object):
    def numRabbits(self, answers):
        """
        :type answers: List[int]
        :rtype: int
        """

        counts = {}
        for a in answers:
            counts[a] = counts.get(a, 0) + 1

        rabbits = 0
        for a, c in counts.items():
            rabbits += int((a + 1) * math.ceil(1.*c / (a + 1)))

        return rabbits



import math
import sys
from utils.templates import fail_string

def unit_test():
    pass

def test():
    # root = TreeNode(4)

    # root.left = TreeNode(2)
    # root.right = TreeNode(6)

    # root.left.left = TreeNode(1)
    # root.left.right = TreeNode(3)

    # solution = Solution_1()
    # print solution.minDiffInBST(root)


    root = TreeNode(1)

    root.left = TreeNode(0)
    root.right = TreeNode(48)

    root.right.left = TreeNode(12)
    root.right.right = TreeNode(49)

    solution = Solution_1()
    print solution.minDiffInBST(root)

def test2():
    solution = Solution_2()

    res = solution.numRabbits([1, 1, 2])
    assert res == 5, res

    res = solution.numRabbits([10, 10, 10])
    assert res == 11, res

    res = solution.numRabbits([])
    assert res == 0, res


    res = solution.numRabbits([2, 2, 2, 2])
    assert res == 6, res

    res = solution.numRabbits([2, 2, 2, 2, 3, 3, 3, 3, 3])
    assert res == 14, res

    res = solution.numRabbits([1, 0, 1, 0, 0])
    assert res == 5, res

if __name__ == '__main__':
    # test()
    # unit_test()
    test2()