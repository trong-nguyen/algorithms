#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Binary search tree classes
"""

class BinaryNode(object):
    """docstring for BinaryNode"""
    def __init__(self, value=None):
        super(BinaryNode, self).__init__()
        self.value = value
        self.parent = None
        self.left = None
        self.right = None

class ColorNode(BinaryNode):
    """
    docstring for ColorNode
    0 for black
    1 for red
    """
    BLACK = -1
    RED = 1
    def __init__(self, value, color=None):
        super(ColorNode, self).__init__(value)
        self.color = color



class BinarySearchTree(object):
    """docstring for BinarySearchTree"""
    Node = BinaryNode
    def __init__(self):
        super(BinarySearchTree, self).__init__()
        self.root = None

    def insert(self, value):
        root = self.root

        cursor = self.walk_to(value)

        # if a node with identical value already present
        # return that node
        if cursor and cursor.value == value:
            return cursor

        node = self.Node(value)

        # if cursor is None, we are at the root
        # replace the root with the actual node
        if cursor is None:
            self.root = node
            return self.root

        # else insert the node to either left or right
        # of the parent node (cursor)
        node.parent = cursor

        if cursor.left is None:
            cursor.left = node
        else:
            cursor.right = node

        # for efficiency, we return the inserted node
        # for inherited class
        return node

    def walk_to(self, value):
        """
        Traverse the tree from the root to the node where

        return: the node where `node.value == value`
        or: the closest parent node
        """
        cursor = self.root

        while cursor and cursor.value != value:
            child = [cursor.left, cursor.right][value > cursor.value]
            if child is None:
                break
            else:
                cursor = child

        return cursor


    def find(self, value):
        if value is None:
            return None

        node = self.walk_to(value)

        if node is None or node.value != value:
            return None

        return node

    def __str__(self):
        output = ''
        heap = [self.root]
        while heap:
            output += str([i.value for i in heap]) + '\n'
            next_heap = []
            for node in heap:
                next_heap += [node.left, node.right]
            next_heap = filter(bool, next_heap)
            heap = next_heap

        return output


class RedBlackTree(BinarySearchTree):
    """docstring for RedBlackTree"""
    Node = ColorNode
    def __init__(self):
        super(RedBlackTree, self).__init__()

    def insert(self, value):
        inserted = super(RedBlackTree, self).insert(value)
        self.color(inserted)

        return inserted

    def color(self, inserted):
        BLACK = ColorNode.BLACK
        RED = ColorNode.RED

        inserted.color = RED

        # 1
        if inserted.parent is None:
            inserted.color = BLACK
            return

        # 2
        if inserted.parent.color == BLACK:
            return

        # 3
        parent = inserted.parent
        grand = parent.parent

        # if not grand


        uncle = [grand.left, grand.right][parent is grand.left]

        if not uncle:
            parent.color = BLACK
            return

        if uncle.color == RED:
            uncle.color = BLACK

        # case 4
        # parent is red and uncle is black
        assert parent.color == RED and uncle.color == BLACK


    def __str__(self):
        output = ''
        heap = [self.root]
        while heap:
            output += str(['{}:{}'.format(i.value, ['R','B'][i.color==ColorNode.BLACK]) for i in heap]) + '\n'
            next_heap = []
            for node in heap:
                next_heap += [node.left, node.right]
            next_heap = filter(bool, next_heap)
            heap = next_heap

        return output

import random

def test():
    tree = BinarySearchTree()

    n = 100
    for i in range(n-1,-1,-1):
        tree.insert(i)

    print tree

    for i in range(n):
        try:
            assert tree.find(i).value == i
        except AssertionError as e:
            print 'Cannot find', str(i)

    assert tree.find(n) is None

    tree = RedBlackTree()
    for i in range(n):
        tree.insert(random.randint(0, n))
    print tree

if __name__ == '__main__':
    test()


