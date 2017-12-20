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
        """
        root is the higher node (in height) and the parent of the pivot
        pivot is the rotated node and the child of the root
        after rotation root becomes child of pivot
        left rotation pivot is on the right
        right rotation pivot is on the left
        diagram https://upload.wikimedia.org/wikipedia/commons/2/23/Tree_rotation.png
              G          G
              |          |
              R  Left->  P
               \        /
                P      R

              G          G
              |          |
              P  <-Right Root
               \        /
                R      Pivot
        """

        assert direction in [self.RLEFT, self.RRIGHT]

        root = self
        pivot = root.right if direction == self.RLEFT else root.left
        grand = root.parent
        if pivot is None:
            status = (
                '{} rotation error, neighbor empty\n'
                'Root:\n{}\n'
                'Pivot:\n{}\n'
                'Grand:\n{}'
                ).format('Left' if direction == self.RLEFT else 'Right',
                    root, pivot, grand)
            raise ValueError(status)

        if direction == self.RLEFT:
            root.right = pivot.left
            # transfer of middle branch, EASY to forget, serious bug
            middle_branch = pivot.left
            pivot.left = root
        else:
            root.left = pivot.right
            # transfer of middle branch
            middle_branch = pivot.right
            pivot.right = root

        root.parent = pivot
        if middle_branch:
            middle_branch.parent = root



        pivot.parent = grand
        if grand is None:
            return # pivot is root

        # else update parent's children accordingly
        if grand.right is root:
            grand.right = pivot
        else:
            grand.left = pivot


    def has_left_branch(self):
        return self.left is not None

    def has_right_branch(self):
        return self.right is not None

    def __str__(self):
        l, r, p = ['na' if not nb else str(nb.value) for nb in [
            self.left, self.right, self.parent
        ]]
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

    def color_str(self):
        return 'X' if self.color == self.BLACK else 'O'

    def __str__(self):
        l, r, p = ['na' if not nb else '{}|{}'.format(nb.value, nb.color_str()) for nb in [
            self.left, self.right, self.parent
        ]]
        output = '{:^19}'.format(p)
        output += '\n{:<5} {:^7} {:>5}'.format(
            l, '[{}|{}]'.format(self.value, self.color_str()), r)
        return output


class BinarySearchTree(object):
    """docstring for BinarySearchTree"""
    Node = BinaryNode

    def __init__(self):
        super(BinarySearchTree, self).__init__()
        self.root = None
        self.count = 0
        self.height = -1

    def insert(self, value):
        cursor = self.walk_to(value)

        # if a node with identical value already present
        # return that node
        if cursor and cursor.value == value:
            return cursor

        node = self.Node(value)
        self.count += 1

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

    def get_leaves(self):
        if not self.root:
            return []

        queue = [self.root]
        leaves = []
        while queue:
            next_queue = []
            for node in queue:
                children = node.children()
                if not children:
                    leaves.append(node)
                else:
                    next_queue += children
            queue = next_queue

        return leaves




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
        precount = self.count
        inserted = super(RedBlackTree, self).insert(value)
        if self.count == precount: # not inserted
            return inserted

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
        if inserted.color == RED and inserted.parent.color == BLACK:
            print '2'
            return

        parent = inserted.parent
        grand = parent.parent
        uncle = [grand.left, grand.right][parent is grand.left]

        # 3
        if uncle is not None and uncle.color == RED:
            print '3'
            parent.color = BLACK
            uncle.color = BLACK
            grand.color = RED
            print self
            self.color(grand)
            return

        # 4
        else:
            # step 1
            # the node was inserted in-order in between his parent and his grand
            # parent and him on the left branch of the grand

            # tree = RedBlackTree()
            # tree.set_root(grand)
            # print 'INNNER TREE'
            # print tree

            # inserted is promoted from the bottom to above grand
            if grand.has_left_branch() and inserted is grand.left.right:
                parent.rotate(BinaryNode.RLEFT)
                grand.rotate(BinaryNode.RRIGHT)

                # switch color
                grand.color = ColorNode.RED
                inserted.color = ColorNode.BLACK
                print '4-1a'
            #                on the right branch
            elif grand.has_right_branch() and inserted is grand.right.left:
                parent.rotate(BinaryNode.RRIGHT)
                grand.rotate(BinaryNode.RLEFT)

                # switch color
                grand.color = ColorNode.RED
                inserted.color = ColorNode.BLACK
                print '4-1b'

            # parent is promoted to above grand
            # or the node was inserted at the right or left most of the branch
            else:
                print '4-2'
                print grand
                print parent
                print inserted
                if parent is grand.left:
                    grand.rotate(BinaryNode.RRIGHT)
                elif parent is grand.right:
                    grand.rotate(BinaryNode.RLEFT)
                else:
                    raise ValueError('Wrong color')

                parent.color = ColorNode.BLACK
                grand.color = ColorNode.RED

            # root can only be changed if rotations are involved
            self.correct_root()

    def correct_root(self):
        if not self.root:
            return None

        while self.root.parent is not None:
            self.root = self.root.parent

        return self.root

    def set_root(self, root):
        assert root is not None, 'Set root must exist'
        assert root.parent is None, 'Set root must not have parent'

        self.root = root
        self.height, self.count = self.statistics()

    def statistics(self):
        if not self.root:
            return 0, 0

        height = 0
        queue = [self.root]
        count = 1
        height = 0
        while queue:
            next_queue = []
            for node in queue:
                next_queue += node.children()

            height += 1
            count += len(next_queue)
            queue = next_queue
        return height, count

    def assert_equal_black_height(self):
        def get_black_height(node, mem):
            if node.value in mem:
                return mem[node.value]
            if not node.parent:
                mem[node.value] = 1
                return 1

            if node.parent.value not in mem:
                get_black_height(node.parent, mem)

            h = int(node.color == ColorNode.BLACK) + mem[node.parent.value]

            # print node
            # print 'Height', node.value, h, mem[node.parent.value], node.parent.value

            mem[node.value] = h
            return h


        leaves = self.get_leaves()
        if not leaves:
            return True

        mem = {}
        h0 = get_black_height(leaves[0], mem)
        for i in range(1, len(leaves)):
            h = get_black_height(leaves[i], mem)
            if h != h0:
                print [l.value for l in leaves]
                print mem
                raise ValueError('Height unbalanced at node {} ({}) wrt h0 {}'.format(leaves[i].value, h, h0))

        return True


    def clone(self, spaces):
        """
        create a cloned tree with space delimiters
        """
        def make_clone_node(idx, original_node):
            return BinaryNode({
                'idx': idx,
                'val': '' if not original_node else '{}:{}'.format(
                    original_node.value, original_node.color_str()
                    )
            })

        n = spaces
        cloned_root = make_clone_node(idx=n/2, original_node=self.root)
        cloned_heap = [cloned_root]
        heap = [self.root]
        height = 0
        while heap:
            height += 1
            if height > self.count:
                print 'excessive tree height'
                return
            next_heap = []
            next_clones = []
            unit = n / (2 ** (height+1))
            if unit <= 0:
                # print(
                #     'Warning, unbalanced tree: n={}'
                #     ', current height={}'
                # ).format(self.count, height)
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
        height, count = self.statistics()
        n = 4 * height

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
    tree.set_root(nodes[3])

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
    tree.set_root(nodes[3])

    nodes[2].rotate(BinaryNode.RRIGHT)

    assert nodes[1].parent is nodes[3]
    assert nodes[2].parent is nodes[1]
    assert nodes[1].parent is nodes[3]
    assert nodes[3].left is nodes[1]
    assert not nodes[2].children(), nodes[1]
    assert not nodes[1].left
    assert not nodes[3].right

def test_binary_tree():
    tree = BinarySearchTree()

    n = 100
    for i in range(n-1, -1, -1):
        tree.insert(i)

    print tree

    for i in range(n):
        try:
            assert tree.find(i).value == i
        except AssertionError as e:
            print 'Cannot find', str(i)

    assert tree.find(n) is None

def test_red_black_tree():
    n = 16
    left_tree = RedBlackTree()
    for i in range(n):
        left_tree.insert(n-i)
    print left_tree

    right_tree = RedBlackTree()
    for i in range(n):
        right_tree.insert(i)
    print right_tree

def test_red_black_height():
    # bug_values = [2003, 467, 1322, 1773, 1311, 450, 1016, 1223, 736, 78, 985, 1243, 841, 2017, 1536, 941, 1814, 756, 1426, 363, 824, 1815, 2040, 1201, 2025, 1887, 1346, 879, 1644, 2010, 257, 376, 1019, 373, 115, 672, 65, 1918, 213, 25, 1451, 948, 1765, 897, 1328, 1517, 1887, 1858, 113, 259, 713, 1302, 1110, 368, 667, 312, 478, 1731, 1994, 1120, 331, 1528, 838, 1038, 1998, 115, 1180, 2048, 875, 138, 652, 33, 511, 104, 853, 1245, 1236, 1027, 1110, 484, 1192, 1813, 1551, 700, 775, 1325, 1887, 1255, 725, 519, 1922, 844, 1805, 283, 480, 1703, 1809, 543, 1732, 488, 1935, 467, 1892, 2006, 2010, 806, 1809, 327, 285, 780, 1458, 1268, 933, 1376, 893, 1379, 563, 1283, 916, 1633, 1226, 1216, 515, 898, 643, 1497, 1155, 1624, 51, 824, 911, 1867, 761, 1056, 748, 1759, 1566, 286, 1187, 521, 1259, 434, 867, 1118, 683, 1452, 798, 158, 896, 130, 971, 1025, 422, 690, 1968, 1228, 1658, 1711, 1499, 264, 968, 444, 1917, 1214, 1569, 1698, 17, 1275, 1908, 462, 1450, 1336, 1811, 125, 1565, 1399, 1398, 787, 506, 98, 252, 635, 1236, 285, 286, 1496, 1105, 639, 2032, 1852, 827, 993, 1909, 1378, 1388, 1773, 1522, 537, 1047, 819, 1128, 414, 367, 2031, 1581, 1040, 437, 1593, 483, 651, 306, 1515, 1467, 983, 1487, 686, 842, 710, 2031, 528, 1342, 2006, 968, 439, 185, 49, 1629, 285, 1389, 1106, 1060, 1401, 969, 1930, 1477, 1465, 1556, 1996, 745, 1104, 1885, 1725, 984, 430, 1131, 2012, 159, 1946, 207, 487, 459, 179, 1792, 592, 1237, 1406, 974, 1354, 1536, 1692, 2002, 1076, 223, 1743, 760, 57, 2036, 1487, 1458, 1756, 1968, 1764, 563, 1538, 914, 226, 1919, 2010, 1091, 1076, 1187, 318, 95, 315, 1907, 611, 1125, 1152, 1829, 137, 1285, 109, 603, 22, 1393, 1768, 914, 375, 34, 1876, 1027, 668, 1603, 1283, 1212, 339, 821, 271, 1597, 856, 255, 1122, 641, 1943, 546, 484, 1234, 1086, 300, 1737, 1976, 821, 1935, 1324, 1409, 127, 1885, 1333, 1299, 1940, 1382, 441, 1552, 1030, 894, 731, 866, 1278, 1752, 472, 510, 1531, 856, 1183, 799, 1107, 2034, 1966, 1295, 1986, 910, 1602, 1357, 175, 1715, 81, 1807, 1517, 828]
    bug_values = [757, 569, 461, 711, 449, 873, 892, 965, 991, 45, 305, 659, 475, 588, 409, 77, 840, 433, 974, 1017, 879, 404, 808, 695, 53, 93, 642, 667, 605, 801, 548, 420, 1020, 416, 704, 1024, 836, 145, 542, 374, 922, 172, 738, 37, 151, 414, 668, 477, 543, 339, 353, 984, 639, 428, 457, 439, 94, 858, 68, 969, 883, 72, 658, 204, 69, 481, 395, 811, 894, 954, 469, 850, 642, 615, 195, 542, 601, 219, 6, 375, 476, 246, 255, 382, 943, 489, 470, 390, 603, 778, 601, 506, 263, 179, 75, 624, 425, 971, 584, 795, 914, 299, 779, 909, 1016, 146, 810, 271, 709, 783, 5, 901, 58, 236, 410, 178, 249, 908, 499, 620, 701, 447, 613, 330, 924, 916, 18, 497, 920, 888, 669, 88, 758, 221, 881, 25, 528, 871, 105, 772, 63, 274, 828, 182, 186, 429, 918, 917, 431, 673, 462, 463, 1010, 779, 95, 79, 40, 180, 835, 820, 989, 382, 614, 677, 333, 740, 28, 82, 356, 229, 160, 371, 696, 876, 654, 236, 319, 341, 452, 220, 652, 420, 379, 312, 287, 335, 571, 725, 995, 558, 816, 740, 455, 361, 132, 114, 760, 989, 49, 974, 269, 105, 362, 429, 315, 940, 351, 772, 266, 243, 788, 703, 800, 30, 107, 955, 854, 416, 657, 904, 195, 312, 344, 698, 165, 313, 1021, 690, 535, 352, 388, 421, 72, 851, 209, 290, 794, 511, 331, 308, 306, 154, 170, 954, 163, 885, 883, 179, 35, 498, 587, 824, 135, 167, 55, 453, 643, 815, 731, 575, 25, 49, 238, 761, 251, 699, 37, 218, 391, 26, 4, 638, 388, 495, 212, 372, 320, 879, 586, 70, 31, 129, 783, 229, 346, 924, 420, 428, 462, 675, 413, 330, 999, 700, 838, 1017, 164, 167, 245, 824, 668, 708, 364, 941, 978, 941, 324, 834, 1001, 663, 704, 873, 293, 891, 43, 164, 604, 878, 304, 442, 378, 546, 448, 505, 506, 885, 388, 89, 232, 500, 795, 265, 921, 678, 890, 969, 140, 460, 148, 66, 962, 683, 483, 59, 762, 612, 418, 997, 127, 736, 1001, 677, 100, 616, 571, 94, 370, 557, 84, 192, 573, 638, 833, 155, 120, 17, 333, 308, 159, 324, 242, 60, 971, 801, 662, 295, 4, 966, 652, 222, 867, 410, 531, 1022, 632, 882, 594, 644, 920, 455, 475, 344, 162, 684, 999, 75, 454, 789, 117, 182, 859, 270, 43, 349, 279, 447, 113, 40, 96, 915, 960, 121, 407, 895, 931, 967, 118, 222, 688, 920, 938, 935, 953, 382, 710, 882, 418, 517, 962, 53, 67, 913, 724, 889, 195, 536, 1024, 801, 75, 213, 919, 487, 960, 751, 618, 169, 911, 593, 480, 267, 341, 572, 526, 429, 620, 432, 481, 356, 720, 869, 936, 219, 668, 125, 252, 614, 641, 936, 409, 607, 407, 476, 361, 66, 319, 290, 272, 110, 154, 608, 87, 798, 928, 894, 289, 763, 246, 588, 199, 782, 754, 1007, 686, 357, 368, 909, 548, 464, 321, 626, 414, 301, 713, 226, 100, 706, 193, 752, 748, 190, 355, 223, 789, 792, 733, 144, 679, 982, 102, 354, 518, 109, 848, 234, 447, 289, 425, 343, 773, 595, 234, 266, 891, 398, 536, 587, 973, 939, 502, 121, 357, 582, 421, 705, 204, 839, 992, 380, 508, 443, 48, 135, 362, 322, 37, 728, 680, 385, 156, 607, 470, 298, 354, 245, 211, 134, 828, 588, 690, 855, 137, 294, 388, 179, 287, 903, 80, 455, 49, 216, 1019, 62, 402, 919, 638, 150, 662, 783, 213, 631, 641, 258, 387, 866, 824, 560, 898, 477, 856, 853, 762, 506, 31, 577, 565, 383, 760, 66, 191, 39, 706, 279, 463, 697, 1016, 206, 346, 885, 96, 252, 431, 203, 1010, 724, 759, 555, 540, 509, 720, 529, 710, 643, 773, 900, 446, 435, 782, 724, 405, 902, 977, 243, 410, 951, 912, 866, 966, 203, 720, 623, 783, 219, 903, 981, 645, 873, 400, 768, 712, 370, 285, 821, 410, 565, 473, 398, 512, 976, 241, 407, 860, 819, 756, 798, 466, 443, 165, 919, 944, 790, 684, 646, 978, 1002, 371, 16, 502, 514, 94, 922, 29, 490, 170, 26, 787, 24, 702, 190, 516, 802, 297, 261, 305, 609, 979, 814, 462, 835, 692, 380, 490, 712, 23, 976, 876, 773, 165, 359, 806, 410, 42, 437, 22, 186, 988, 881, 462, 822, 858, 79, 941, 563, 43, 725, 233, 697, 770, 207, 603, 985, 952, 606, 10, 655, 992, 391, 52, 215, 77, 889, 129, 884, 866, 853, 160, 278, 754, 776, 85, 834, 495, 900, 272, 973, 22, 941, 971, 936, 752, 62, 447, 127, 56, 995, 552, 37, 257, 70, 918, 367, 672, 486, 953, 421, 490, 356, 896, 482, 361, 402, 305, 831, 46, 467, 523, 158, 30, 535, 691, 202, 42, 655, 134, 135, 249, 101, 537, 805, 769, 265, 59, 650, 766, 217, 291, 945, 208, 113, 875, 196, 364, 35, 451, 102, 91, 214, 70, 788, 818, 945, 179, 853, 321, 40, 978, 311, 644, 715, 488, 839, 226, 800, 954, 33, 298, 347, 359, 637, 126, 543, 244, 150, 605, 956, 718, 507, 757, 146, 1002, 362]
    tree = RedBlackTree()
    for v in bug_values:
        tree.insert(v)
        tree.assert_equal_black_height()

    # for d in range(1, 15):
    # # for d in [8]:
    #     n = 2 ** d
    #     values = []
    #     tree = RedBlackTree()
    #     for i in range(n):
    #         # tree.insert(i)
    #         try:
    #             values.append(random.randint(0, n))
    #             tree.insert(values[-1]) # CHECK THIS, OVERLAP ITEMS CAUSE PROBLEMS
    #         except:
    #             print 'inserting', values
    #             print tree
    #             raise


    #     h, c = tree.statistics()
    #     print 'Tree height x count: {:>3} x {}'.format(h, c)




if __name__ == '__main__':
    # test_rotate_left()
    # test_rotate_right()
    # test_binary_tree()
    # test_red_black_tree()
    test_red_black_height()
