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

    def children(self):
        c = []
        if self.left:
            c += self.left
        if self.right:
            c += self.right
        return c

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

        if value < cursor.value:
            cursor.left = node
        elif value > cursor.value:
            cursor.right = node
        else:
            raise ValueError('identical value found')

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

        parent = inserted.parent
        grand = parent.parent
        uncle = [grand.left, grand.right][parent is grand.left]

        # 3
        if uncle is not None and uncle.color == RED:
            parent.color = BLACK
            uncle.color = BLACK

        # 4
        # None is considered black
        if uncle is None or uncle.color == BLACK:
            return

        # 4
        if not uncle:
            parent.color = BLACK
            return

        if uncle.color == RED:
            uncle.color = BLACK

        # case 4
        # parent is red and uncle is black
        assert parent.color == RED and uncle.color == BLACK


    def clone(self, spaces):
        """
        create a cloned tree with space delimiters
        """
        def make_clone_node(idx, original_node):
            return BinaryNode({
                'idx': idx,
                'val': '' if not original_node else '{}:{}'.format(original_node.value, ['O', 'X'][original_node.color==ColorNode.BLACK])
            })

        n = spaces
        cloned_root = make_clone_node(idx=n, original_node=self.root)
        cloned_heap = [cloned_root]
        heap = [self.root]
        height = 0
        while heap:
            height += 1
            next_heap = []
            next_clones = []
            unit = n / (2 ** height)
            if unit <= 0:
                raise ValueError('increase spaces for cloning, {} insufficient, reached height {}'.format(spaces, height))

            for node, cloned_node in zip(heap, cloned_heap):
                if node.left:
                    cloned_node.left = make_clone_node(
                        idx=cloned_node.value['idx'] - unit,
                        original_node=node.left,
                    )
                    print cloned_node.left.value
                    next_heap.append(node.left)
                    next_clones.append(cloned_node.left)
                if node.right:
                    cloned_node.right = make_clone_node(
                        idx=cloned_node.value['idx'] + unit,
                        original_node=node.right,
                    )
                    print cloned_node.right.value
                    next_heap.append(node.right)
                    next_clones.append(cloned_node.right)

            print [h.value for h in heap], height
            heap = filter(bool, next_heap)
            cloned_heap = filter(bool, next_clones)

        return cloned_root

    def __str__(self):
        n = 2**6
        cell = 6
        cell_form = '{{:{}}}'.format(cell)
        cloned_root = self.clone(n)
        heap = [cloned_root]
        output = []
        while heap:
            row = list(' ' * n * cell)
            next_heap = []
            for node in heap:
                next_heap += [node.left, node.right]
                meta = node.value
                s = cell_form.format(meta['val'])
                offset = meta['idx']
                row[offset:offset+cell] = list(s)

            output.append(''.join(row))
            heap = filter(bool, next_heap)

        return '\n'.join(output)

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
    for i in range(16):
        tree.insert(random.randint(0, 16))
    print tree

if __name__ == '__main__':
    test()


