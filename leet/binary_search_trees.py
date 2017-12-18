#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Binary search tree classes
"""


class BinaryNode(object):
    """docstring for BinaryNode"""
    RLEFT = 1 # rotate anti-clockwise
    RRIGHT = -1 # rotate clock-wise

    def __init__(self, value=None):
        super(BinaryNode, self).__init__()
        self.value = value
        self.parent = None
        self.left = None
        self.right = None

    def children(self):
        c = []
        if self.left:
            c.append(self.left)
        if self.right:
            c.append(self.right)
        return c

    def rotate(self, direction):
        assert direction in [self.RLEFT, self.RRIGHT]

        center = self
        rotatee = center.right if direction == self.RLEFT else center.left
        parent = center.parent
        assert rotatee is not None, 'Rotation error, neighbor empty'

        if direction == self.RLEFT:
            center.right = rotatee.left
            center.parent, rotatee.left = rotatee, center
        else:
            center.left = rotatee.right
            center.parent, rotatee.right = rotatee, center



        rotatee.parent = parent
        if parent is None:
            return # center is root

        # else update parent's children accordingly
        if parent.right is center:
            parent.right = rotatee
        else:
            parent.left = rotatee


    def has_left_branch(self):
        return self.left is not None

    def has_right_branch(self):
        return self.right is not None

    def __str__(self):
        l = 'na' if not self.left else str(self.left.value)
        r = 'na' if not self.right else str(self.right.value)
        p = 'na' if not self.parent else str(self.parent.value)
        output = '{:^19}'.format(p)
        output += '\n{:<5} {:^7} {:>5}'.format(l, '[{}]'.format(self.value), r)
        return output


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
        self.count = 0

    def insert(self, value):
        cursor = self.walk_to(value)

        # if a node with identical value already present
        # return that node
        if cursor and cursor.value == value:
            return cursor

        self.count += 1
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
                next_heap += node.children()
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
        inserted.color = ColorNode.RED
        self.color(inserted)

        return inserted

    def color(self, inserted):
        """
        https://en.wikipedia.org/wiki/Red–black_tree
        """
        BLACK = ColorNode.BLACK
        RED = ColorNode.RED

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
            return

        # 4
        # None is considered black
        if uncle is None or uncle.color == BLACK:
            node = inserted
            # step 1
            if grand.has_left_branch() and inserted is grand.left.right:
                parent.rotate(BinaryNode.RLEFT)
                node = parent.left
            elif grand.has_right_branch() and inserted is grand.right.left:
                parent.rotate(BinaryNode.RRIGHT)
                node = parent.right

            # step 2
            if node is node.parent.left:
                grand.rotate(BinaryNode.RRIGHT)
            else:
                try:
                    grand.rotate(BinaryNode.RLEFT)
                except:
                    print self
                    raise

            # switch color
            grand.color = ColorNode.RED
            inserted.color = ColorNode.BLACK


        self.correct_root()

    def correct_root(self):
        if not self.root:
            return None

        while self.root.parent is not None:
            self.root = self.root.parent

        return self.root


    def clone(self, spaces):
        """
        create a cloned tree with space delimiters
        """
        def make_clone_node(idx, original_node):
            return BinaryNode({
                'idx': idx,
                'val': '' if not original_node else '{}:{}'.format(
                    original_node.value,
                    ['O', 'X'][original_node.color == ColorNode.BLACK]
                )
            })

        n = spaces
        cloned_root = make_clone_node(idx=n/2, original_node=self.root)
        cloned_heap = [cloned_root]
        heap = [self.root]
        height = 0
        while heap:
            print [h.value for h in heap]
            height += 1
            if height > self.count:
                print 'excessive tree height'
                return
            next_heap = []
            next_clones = []
            unit = n / (2 ** (height+1))
            if unit <= 0:
                print(
                    'Warning, unbalanced tree: n={}'
                    ', current height={}'
                ).format(self.count, height)
                unit = 1

            for node, cloned_node in zip(heap, cloned_heap):
                if node.left:
                    cloned_node.left = make_clone_node(
                        idx=cloned_node.value['idx'] - unit,
                        original_node=node.left,
                    )
                    next_heap.append(node.left)
                    next_clones.append(cloned_node.left)
                if node.right:
                    cloned_node.right = make_clone_node(
                        idx=cloned_node.value['idx'] + unit,
                        original_node=node.right,
                    )
                    next_heap.append(node.right)
                    next_clones.append(cloned_node.right)

            heap = filter(bool, next_heap)
            cloned_heap = filter(bool, next_clones)

        return cloned_root

    def __str__(self):
        # compute necessary capacity
        n = 2
        while n < self.count:
            n *= 2

        cell = 3
        cell_form = '{{:{}}}'.format(cell)
        cloned_root = self.clone(n)
        if cloned_root is None:
            raise ValueError('Cloned root is empty')
        heap = [cloned_root]
        output = []
        while heap:
            row = list(' ' * n * cell)
            next_heap = []
            for node in heap:
                next_heap += node.children()
                meta = node.value
                s = cell_form.format(meta['val'])
                offset = meta['idx'] * cell
                row[offset:offset+cell] = list(s)

            output.append(''.join(row))
            heap = filter(bool, next_heap)

        return '\nRED-BLACK tree visualization:\n' + '\n'.join(output)

import random

def test_rotate_left():
    nodes = map(ColorNode, range(10))

    nodes[1].right, nodes[2].parent = nodes[2], nodes[1]
    nodes[1].parent, nodes[3].left = nodes[3], nodes[1]

    tree = RedBlackTree()
    tree.count = 3
    tree.root = nodes[3]

    nodes[1].rotate(BinaryNode.RLEFT)

    assert nodes[1].parent is nodes[2]
    assert nodes[2].left is nodes[1]
    assert nodes[2].parent is nodes[3]
    assert nodes[3].left is nodes[2]
    assert not nodes[1].children(), nodes[1]
    assert not nodes[2].right
    assert not nodes[3].right

def test_rotate_right():
    nodes = map(ColorNode, range(10))

    nodes[1].parent, nodes[2].left = nodes[2], nodes[1]
    nodes[2].parent, nodes[3].left = nodes[3], nodes[2]

    tree = RedBlackTree()
    tree.count = 3
    tree.root = nodes[3]

    nodes[2].rotate(BinaryNode.RRIGHT)

    assert nodes[1].parent is nodes[3]
    assert nodes[2].parent is nodes[1]
    assert nodes[1].parent is nodes[3]
    assert nodes[3].left is nodes[1]
    assert not nodes[2].children(), nodes[1]
    assert not nodes[1].left
    assert not nodes[3].right

def test():
    # tree = BinarySearchTree()

    # n = 100
    # for i in range(n-1, -1, -1):
    #     tree.insert(i)

    # print tree

    # for i in range(n):
    #     try:
    #         assert tree.find(i).value == i
    #     except AssertionError as e:
    #         print 'Cannot find', str(i)

    # assert tree.find(n) is None


    left_tree = RedBlackTree()
    for i in range(6):
        left_tree.insert(6-i)
    print left_tree

    right_tree = RedBlackTree()
    for i in range(6):
        right_tree.insert(i)
    print right_tree

if __name__ == '__main__':
    test_rotate_left()
    test_rotate_right()
    test()
