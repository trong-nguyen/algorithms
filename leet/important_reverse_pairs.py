#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given an array nums, we call (i, j) an important reverse pair if i < j and nums[i] > 2*nums[j].

You need to return the number of important reverse pairs in the given array.

Example1:

Input: [1,3,2,3,1]
Output: 2
Example2:

Input: [2,4,3,5,1]
Output: 3
Note:
The length of the given array will not exceed 50,000.
All the numbers in the input array are in the range of 32-bit integer.

"""

import sys
from utils.templates import fail_string
from utils.bst import RedBlackTree

class CountNode(RedBlackTree.Node):
    """
    A node class that added a count field for the subbranch including itself
    """
    def __init__(self, *arg):
        super(CountNode, self).__init__(*arg)
        self.count = 1 # itself

    def rotate(self, direction):
        # adjust count field for rotations
        super(CountNode, self).rotate(direction)

        # this is after rotation
        if direction == self.RLEFT:
            middle_branch = self.right
        else:
            middle_branch = self.left

        pivot = self.parent
        pivot_count = pivot.count
        root_count = self.count
        middle_branch_count = 0 if not middle_branch else middle_branch.count

        pivot.count += root_count - pivot_count
        self.count += - pivot_count + middle_branch_count

    def render(self):
        s = super(RedBlackTree.Node, self).render()
        return '{}|{}'.format(s, self.count)

class CountTree(RedBlackTree):
    """
    A BST that maintains a counting of nodes on the subtree
    """
    Node = CountNode
    def __init__(self, *arg):
        super(CountTree, self).__init__(*arg)

    def insert(self, value):
        # first insert the node as usual
        precount = self.count
        inserted = super(RedBlackTree, self).insert(value)
        if self.count == precount:
            # if no new node inserted no maintenance required (color, count)
            return inserted

        # else maintain the count due to the inserted node
        # all the node on the path from inserted to root increases by 1
        cursor = inserted
        while cursor.parent:
            cursor = cursor.parent
            cursor.count += 1

        # correct color (and also counts if rotations involved)
        self.color(inserted)

        return inserted

    def count_lesser_or_equal_to(self, value):
        cursor = self.walk_to(value)

        # travers back up until a cursor with value smaller is found
        while cursor and cursor.value > value:
            cursor = cursor.parent

        if not cursor:
            # value is larger than the entire tree
            return 0

        # now we can be sure that cursor.value is larger than or equal to value
        # in other words, cursor is at or on the left tree of the node with given value
        def get_left_count(pos):
            if not pos:
                return 0

            return 1 if not pos.left else (pos.left.count + 1)

        lesser = get_left_count(cursor)
        while cursor and cursor.parent:
            if cursor is cursor.parent.right:
                lesser += get_left_count(cursor.parent)

            cursor = cursor.parent

        return lesser


def reverse_pairs(nums):
    """
    """
    # sort, keeping the order
    array = sorted(enumerate(nums), cmp=lambda a, b: a[0] <= b[0] and a[1] > 2 * b[1])

    # iterate and count
    pairs = 0
    for i in range(len(array) - 1):
        pass


    # count the one that satisfy order and mag conditions


class Solution(object):
    def reversePairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        pass

import random
def test_tree():
    print 'Test Count tree ...'
    n = 2**10
    tree = CountTree()
    for i in range(n):
        tree.insert(random.randint(0, n*10))

    height, total = tree.statistics()
    print 'Total inserted entries: {}, height {}, root count {}'.format(
        total, height, tree.root.count
        )
    assert tree.root.count == total

def test_counting():
    print 'Test counting functionalities ...'
    n = 2**12
    tree = CountTree()
    values = set()
    for i in range(n):
        v = random.randint(0, n)
        values.add(v)
        tree.insert(v)

    values_list = sorted(values)
    for i in range(n/10):
        v = random.randint(0, n)
        if v in values:
            res = tree.count_lesser_or_equal_to(v-1) # means strictly less than v
            # print 'Counting less than: {}, res {}'.format(v, res)
            assert res == values_list.index(v) # index indicates pos or how many before it

def test():
    for case, ans in [
        ([[1,3,2,3,1]], 2),
        ([[2,4,3,5,1]], 3),
    ]:
        res = function(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test_tree()
    test_counting()
    # test()