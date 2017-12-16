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
        self.color = color if color != None else self.BLACK



class BinarySearchTree(object):
    """docstring for BinarySearchTree"""
    Node = BinaryNode
    def __init__(self):
        super(BinarySearchTree, self).__init__()
        self.root = self.Node(None)

    def insert(self, value):
        root = self.root
        if root.value is None:
            root.value = value
            return

        cursor = self.root
        while True:
            child = [cursor.left, cursor.right][value >= cursor.value]
            if child is None:
                break
            else:
                cursor = child

        node = self.Node(value)
        node.parent = cursor

        if cursor.left is None:
            cursor.left = node
        else:
            cursor.right = node


    def find(self, value):
        pass

    def __str__(self):
        output = ''
        heap = [self.root]
        while heap:
            output += str([i.value for i in heap])
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
        self.root.color = ColorNode.BLACK

    def insert(self, value):
        super(RedBlackTree, self).insert(value)

def test():
    tree = BinarySearchTree()
    for i in range(100,0,-1):
        tree.insert(i)
    print tree

    tree = RedBlackTree()
    for i in range(100):
        tree.insert(i)
    print tree

if __name__ == '__main__':
    test()


