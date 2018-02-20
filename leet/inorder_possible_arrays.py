#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def possible_bst_arrays(root):
    """
    find the possible initial arrays that made the tree rooted at root

    recursively intertwining left and right branches
    the only constraint for the possible initial arrays is that the parent nodes must
    appear before child nodes
    i.e.
    a tree

      2
     / \
    1   3
    could be the result of initial arrays [2, 1, 3] or [2, 3, 1]
    The constraint is that 1 and 3 must appear after 2, the relative order between left and right
    branches are not important.
    This is analogous to the intertwining problem where
    we need to decide that if an array c is an intertwined version of a and b
    so the answer is that the relative order of a elements ai or b elements bi must be preserved in c
    """
    if not root:
        return []

    left_branch = possible_bst_arrays(root.left)
    right_branch = possible_bst_arrays(root.right)

    if not root.left:
        sub = right_branch
    elif not root.right:
        sub = left_branch
    else:
        sub = []
        for l in left_branch:
            for r in right_branch:
                sub += weave(l, r)

    r = [root.value]
    if sub:
        return [r + a for a in sub]
    else:
        return [r]

def weave(a, b):
    """
    rtype: an array of arrays, all possible weaved together a and b
    """
    result = []
    for x, y in [(a, b), (b, a)]:
        if x:
            r = weave(x[1:], y)
            prefix = [x[0]]
            result += [prefix] if not r else [prefix + i for i in r]

    return result

import sys
from utils.templates import fail_string

def unit_test():
    print weave([1, 3, 5], [2, 4])
    print weave([2], [0])


    node = Node(1)
    node.left = Node(0)
    node.right = Node(2)

    assert sorted(possible_bst_arrays(node)) == sorted([[1, 0, 2], [1, 2, 0]])

    node = Node(2)
    node.left = Node(1)
    node.right = Node(4)
    node.left.left = Node(0)
    node.right.left = Node(3)
    node.right.right = Node(5)

    assert sorted(possible_bst_arrays(node)) == sorted([[2, 1, 0, 4, 3, 5], [2, 1, 4, 3, 5, 0], [2, 1, 4, 3, 0, 5], [2, 1, 4, 0, 3, 5], [2, 4, 3, 5, 1, 0], [2, 4, 3, 1, 0, 5], [2, 4, 3, 1, 5, 0], [2, 4, 1, 0, 3, 5], [2, 4, 1, 3, 5, 0], [2, 4, 1, 3, 0, 5], [2, 1, 0, 4, 5, 3], [2, 1, 4, 5, 3, 0], [2, 1, 4, 5, 0, 3], [2, 1, 4, 0, 5, 3], [2, 4, 5, 3, 1, 0], [2, 4, 5, 1, 0, 3], [2, 4, 5, 1, 3, 0], [2, 4, 1, 0, 5, 3], [2, 4, 1, 5, 3, 0], [2, 4, 1, 5, 0, 3]])


    node = Node(4)
    node.left = Node(1)
    node.left.left = Node(0)
    node.left.right = Node(2)
    node.left.right.right = Node(3)

    node.right = Node(5)
    node.right.right = Node(6)

    print possible_bst_arrays(node)
if __name__ == '__main__':
    unit_test()