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

    def insert(self, value, equal_check=True):
        # if cursor is None, we are at the root
        # replace the root with the actual node
        if not self.root:
            self.root = self.Node(value)
            self.count += 1
            return self.root

        cursor = self.root

        path = []
        while cursor:
            path.append(cursor)
            if cursor.value == value:
                return value

            child = [cursor.left, cursor.right][value > cursor.value]
            if child is None:
                break
            else:
                cursor = child

        node = self.Node(value)
        self.count += 1
        if value < cursor.value:
            cursor.left = node
        else:
            cursor.right = node

        # update
        for nd in path:
            nd.count += 1

        # correct color (and also counts if rotations involved)
        self.color(node)

        return node

    def count_larger(self, value):
        cursor = self.root

        # traverse top down until value found or leaves reached
        larger = 0
        while cursor:
            if cursor.value >= value:
                larger += 0 if not cursor.right else cursor.right.count
                if cursor.value == value:
                    return larger

                larger += 1 # including the current cursor node
                cursor = cursor.left
            else:
                cursor = cursor.right

        return larger


def reverse_pairs(nums):
    """
    """
    # sort, keeping the order
    tree = CountTree()
    reverse_count = 0
    n = len(nums)
    for i, v in enumerate(nums):
        if i > 0:
            reverse_count += tree.count_larger((2*v,n))
        tree.insert((v, i))

    return reverse_count


class Solution(object):
    def reversePairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        return reverse_pairs(nums)

import random
def test_tree():
    print 'Test Count tree ...'
    n = 2**12
    tree = CountTree()
    for i in range(n):
        assert tree.count == 0 if not tree.root else tree.root.count
        tree.insert(random.randint(0, n*10))

    height, total = tree.statistics()
    print 'Total inserted entries: {}, height {}, root count {}'.format(
        total, height, tree.root.count
        )
    assert tree.root.count == total

def test_counting():
    print 'Test counting functionalities ...'
    n = 2**10
    tree = CountTree()
    values = set()
    for i in range(n):
        v = random.randint(-n, n)
        values.add(v)
        tree.insert(v)

    values_list = sorted(values)
    assert tree.count_larger(values_list[-1]) == 0
    assert tree.count_larger(values_list[0]) == len(values_list) - 1
    assert tree.count_larger(values_list[0]-1) == len(values_list)
    for i in range(n/10):
        v = random.randint(-n, n)
        if v in values:
            res = tree.count_larger(v) # means strictly less than v
            # print 'Counting less than: {}, res {}'.format(v, res)
            assert res == len(values_list) - 1 - values_list.index(v) # index indicates pos or how many before it

def test():
    for case, ans in [
        ([[-5, -5]], 1),
        ([[1,3,2,3,1]], 2),
        ([[2,4,3,5,1]], 3),
        ([[-185,143,-154,-338,-269,287,214,313,165,-364,-22,-5,9,-212,46,328,-432,-47,317,206,-112,-9,-224,-207,6,198,290,27,408,155,111,-230,-2,-266,84,-224,-317,39,-482,159,35,132,-151,70,-179,104,-156,450,-13,216,190,238,-138,354,171,-398,-36,417,26,-27,-142,478,-362,-91,-262,-11,469,248,-286,-269,-69,-221,-70,26,484,-31,-236,-173,-380,-8,312,-138,-96,23,-7,39,-345,269,156,349,200,52,193,152,168,159,181,272,-259,210,76,194,-31,139,392,-16,-151,50,166,45,9,44,-179,151,-8,75,-277,-18,49,314,-332,449,24,362,88,159,14,-279,232,211,-206,-192,27,238,-339,-79,30,-370,-29,81,251,-189,21,-202,-41,198,51,-6,172,108,26,-168,316,271,-76,-20,-249,-111,47,-86,303,35,127,113,-181,289,-105,-30,-16,-9,95,-144,-422,198,320,7,-227,-161,447,486,-406,-121,-280,-76,285,-453,42,15,-335,-189,-154,280,-206,68,-313,-375,-401,47,184,-320,369,-146,-60,150,378,87,102,138,-54,169,33,-339,-19,147,333,84,92,-57,104,76,-239,99,300,217,-140,153,-344,-103,-6,-37,399,323,-138,279,-259,217,172,-94,-55,29,462,-327,-177,-163,-444,-84,-281,-87,350,-180,20,0,46,331,-15,-244,-370,69,-194,-30,-85,-112,-235,-242,-188,231,123,-233,-29,113,-294,90,64,-3,-364,55,120,-48,-323,99,-76,-70,79,-351,300,-44,-30,25,334,-199,-68,-451,19,57,293,-188,-16,-46,-392,-162,50,-304,23,166,-130,-146,-35,-141,-25,124,-239,114,-104,285,-108,-137,177,-129,-443,341,-112,134,-293,-181,278,203,442,-206,-20,457,-267,171,-321,208,-4,8,-16,-474,-214,-18,-139,-129,-239,-152,45,443,160,-226,338,-384,198,-77,398,296,-405,-156,290,87,-423,-15,-374,127,259,-20,-62,426,-86,-44,184,-207,257,44,-106,-166,260,-181,-282,-68,-90,-39,-3,375,415,20,-207,391,-201,-143,60,242,-192,-74,426,-86,1,74,208,107,-92,114,-37,145,-216,99,319,-298,124,243,73,-127,-139,56,298,24,-354,30,-166,175,82,187,-24,112,-22,-392,-166,-376,470,139,284,-93,162,-160,89,-240,36,-380,-58,-249,104,-1,-172,198,-70,-381,29,20,305,-197,-253,-145,72,98,-375,-152,91,96,-64,170,142,66,398,97,-19,-298,-175,118,-77,-361,354,-29,-47,71,231,-174,-11,-347,-87,36,-318,50,-157,-182,-348,10,96,-241,-82,473,-50,-10,-75,-148,71,20,119,-37,-188,35,65,-346,50,256,-20,-80,-358,419,6,-341,24,-113,-169,108,-488,-334,249,234,-73,-208,19,-264,-89,-41,66,-3,17,-95,2,-143,-11,-348,-324,-366,-183,-148,-76,-197,201,57,-94,-1,0,43,-6,70,-183,71,-304,58,-35,359,103,238,93,331,59,24,-145,92,-34,3,147,-241,-54,-90,1,313,-116,436,162,258,468,-154,-31,111,207,-484,-19,440,201,9,-230,11,-355,246,-78,295,-84,97,43,317,158,-78,183,132,-265,360,-398,-284,-69,212,112,-236,-111,108,266,200,386,-355,36,-3,-3,304,205,-142,-250,8,-45,-35,-165,54,390,175,-44,-255,-207,-64,431,-186,-279,-126,-65,-211,42,246,27,-302,-342,-386,-193,-123,216,71,-391,-343,3,-15,-486,138,142,463,27,-126,-84,39,188,145,402,-260,41,423,6,-86,10,418,-4,-37,-256,-345,-47,49,314,-169,-81,-351,218,-163,0,-6,-432,189,245,-167,92,2,-83,-176,-312,222,108,-18,-119,193,-84,87,-299,220,2,-323,-61,-300,-142,142,223,90,211,107,326,-43,247,43,-27,-114,187,260,-25,-263,-69,-194,-316,-73,230,95,278,-176,37,134,290,-166,-78,135,259,146,-148,1,-210,-209,-59,-92,89,-216,-250,-411,-181,-78,419,21,-370,-9,-154,-24,-306,57,-27,-254,86,-364,71,-99,-70,-79,141,206,-187,227,-362,-293,81,313,-311,-208,-401,-206,-282,-123,86,3,-22,-324,72,-126,-84,216,-411,19,115,-393,-102,-300,275,-376,30,-403,449,465,-243,-168,-7,-43,-23,-219,149,-43,-14,-139,384,-23,15,-10,-263,-375,156,158,-76,27,-263,50,174,305,22,150,-94,-368,-142,61,119,154,-247,-52,-38,-81,-105,402,-21,-148,2,-28,-164,-387,358,216,168,148,200,4,-222,183,281,-428,-13,2,-289,-459,-188,117,193,140,463,-56,159,29,-250,216,143,12,151,48,174,-105,-83,247,324,-204,-181,71,-184,411,-52,-110,-220,168,46,383,-223,-56,24,322,50,-14,-206,-84,-2,-173,219,150,-356,331,-78,-123,468,-184,243,-160,-96,235,-70,214,253,113,313,-80,201,383,125,83,-124,33,223,-48,-55,-175,-364,-98,52,223,45,90,-23,18,141,71,258,-214,-142,-230,159,-319,-440,219,-217,-72,198,56,240,210,76,22,46,-264,159,-153,-189,-212,317,-420,-71,19,-46,64,-37,-15,-397,-27,-236,-135,268,-223,112,392,-300,371,-209,51,109,-465,-219,-155,-138,77,96,-10,33,77,-366,491,22,83,180,-70,-404,-312,-384,251,8,305,-316,157,-318,435,100,274,123,-180,499,-285,221,-135,-199,145,234,12,-13,-164,133,115,-160,315,149,-36,-164,107,-74,300,-34,246,219,-148,-182,26,-143,-321,73,-140,-395,-119,169,38,-148,290,5,319,-126,61,-289,13,86,98,170,-153,-326,-213,152,23,-19,253,154,-116,-3,191,-13,184,283,-71,-116,-315,278,160,173,-151,199,441,-208,-385,95,-338,179,466,37,-50,386,-343,16,162,88,187,-247,328,201,1,-127,274,-152,117,-50,71,59,-33,141,-245,321,-258,-112,82,40,184,310,359,-92,-176,-65,137,-9,-168,79,-66,106,56,3,-176,83,-379,451,64,-101,-65,-403,-193,-31,109,368,-454,119,-340,175,346,-28,275,-293,107,-262,-311,383,140,-7,70,122,-251,-2,-133,9,157,113,349,151,-94,-37,-24,-340,264,-286,92,23,36,-364,331,-419,-107,-342,63,-65,-364,-262,-19,-271,-259,-123,140,-32,29,-38,-401,-491,41,320,-67,-82,399,-294,176,152,-183,173,185,162,100,399,-255,66,194,178,44,-208,-354,-152,-336,-3,-23,-335,22,-71,-244,-246,166,272,227,-350,221,279,66,253,-493,199,-249,81,-189,102,-91,-197,-445,-206,67,-50,-384,-116,-295,-225,22,-350,-364,24,269,-285,34,-123,5,-207,-482,92,-418,25,280,-330,-351,-79,-87,4,-278,251,71,115,214,-141,128,-193,111,145,-215,-116,-216,114,72,-460,142,67,-171,-252,409,27,-173,152,176,-300,-288,11,270,115,-246,-323,192,18,272,-147,61,114,49,155,33,-160,-134,43,206,322,-96,-89,105,-60,181,-78,-249,123,-30,2,-304,166,72,31,145,-131,222,36,-108,142,69,149,16,167,-85,86,-282,311,57,306,-46,-98,28,107,405,-323,-427,116,-29,-156,99,408,-12,120,-57,79,-204,-162,19,-244,82,-221,178,371,139,309,-278,118,102,175,-429,249,82,182,-231,159,180,113,-128,183,-149,18,-126,-34,-319,24,-220,25,-223,24,136,-373,-58,61,-53,-189,402,-104,-42,43,90,69,174,-22,-197,-183,424,-111,42,210,152,-27,122,350,-358,259,283,-222,131,337,28,-259,108,289,-313,-178,-316,-433,-6,-31,-150,285,-56,6,261,5,484,-76,-77,85,178,-279,87,204,77,65,29,-138,-202,-80,48,-407,-285,-204,358,67,-86,75,55,27,217,-183,-225,280,-55,-74,126,279,-67,116,-297,7,-169,201,-147,314,-268,-469,81,-401,-155,47,314,-175,361,-314,-147,331,340,-121,-42,99,164,36,-158,-82,226,-97,-231,48,-83,-132,158,-147,44,-182,191,-320,268,145,-14,89,144,-213,141,346,-266,148,-286,-10,-97,129,17,-9,84,-141,-326,7,-197,321,-447,110,-80,376,367,-122,331,72,-190,-68,124,268,-44,-20,-120,131,168,151,5,8,-86,-72,-335,-255,-408,36,180,-407,169,213,-292,-223,-244,60,-271,-178,143,-274,25,-466,119,127,-470,-323,392,23,-291,-71,-123,-12,-186,-3,-51,-15,380,389,-204,59,-292,26,-4,83,-5,-19,6,-223,-228,259,122,375,60,21,297,212,240,-220,96,8,19,417,-44,-121,-214,-13,-252,-74,-9,-100,-126,198,19,425,-156,73,338,305,465,-9,-329,-79,-380,-167,-93,-151,-65,-299,122,161,-48,-72,-243,-134,-420,-61,228,-106,240,222,40,194,-248,240,-276,-273,-468,-149,-345,295,-433,60,-425,94,-239,-301,0,460,285,-281,40,-207,442,-89,-277,60,335,169,-472,115,39,-467,234,317,-175,192,-41,-438,-101,283,40,139,-178,1,-4,101,81,-178,-75,-204,27,18,-215,-97,-311,413,-230,-38,290,254,-173,-33,355,-145,-30,-89,-123,168,-118,-328,26,-99,-221,-13,69,60,273,475,18,-396,-134,-140,256,-256,-144,-195,141,-334,483,267,154,-234,134,-195,-277,151,-28,-37,339,-190,-208,185,-242,121,188,329,277,-99,-364,-136,-280,-45,-320,160,-32,182,212,42,237,85,-130,140,-233,187,-13,-171,-1,176,-45,-6,192,-350,-8,78,-241,174,121,-376,-127,-16,249,-335,-271,441,-32,-229,-109,80,-164,141,326,-137,-96,452,351,-322,186,458,-78,152,203,149,-493,-15,-154,-85,78,-240,309,181,37,-189,-178,1,-311,198,55,140,105,260,208,82,-281,32,335,-371,-46,129,-116,45,-225,-61,59,249,125,-193,162,10,25,172,-99,-134,-433,-73,141,-253,125,-260,-67,208,-421,-6,-306,473,306,12,-83,-339,-90,-179,-388,349,-166,165,-169,-37,-132,-43,33,375,-443,12,-377,-140,406,-15,26,45,-207,-173,57,-49,290,109,-254,7,86,-100,90,-15,-84,343,85,-184,359,199,345,-194,-246,397,-173,-281,-154,-2,-9,-50,91,-254,37,147,72,-56,93,121,-14,-52,-124,-148,194,-170,-51,-143,95,143,-97,-292,20,161,-121,-397,70,-28,42,41,-180,86,-12,298,304,-63,65,-43,208,-238,-473,259,16,-275,115,62,-103,-161,-383,-88,-53,349,-114,308,13,62,-263,-198,182,-48,-55,417,-17,-29,271,69,-175,120,-190,-154,-263,-138,5,296,-22,-98,-266,-80,-144,374,-236,-220,334,120,-168,-95,144,-291,-137,-116,59,-154,-87,-175,133,-109,-60,278,-209,102,-237,355,-79,230,45,-2,390,107,-152,29,160,73,-482,-234,445,-181,3,-243,-140,-163,48,-28,410,-98,-226,-148,112,236,-26,380,-246,-189,263,-151,422,-269,135,-238,-238,224,-269,112,-336,-322,-167,-61,-123,-267,-219,-86,-11,-164,70,-229,133,294,98,176,157,242,-98,218,311,-381,247,-223,341,-229,43,394,69,-79,-110,-99,-68,61,159,-98,-139,194,-130,275,-61,-182,-31,313,-75,-32,-252,145,-311,412,117,414,325,170,291,353,-105,354,254,-194,-239,-64,203,-93,161,-298,-274,440,33,-10,266,104,-256,-164,-15,-209,346,-194,176,463,365,379,-66,-46,7,90,236,-225,267,-18,403,43,89,299,146,-241,104,-47,80,-245,299,-38,-57,48,431,-194,91,33,210,-407,-152,244,272,117,-451,383,116,-146,-102,-310,-174,30,-275,-101,5,-52,-74,194,-38,17,-320,-138,-23,-86,-85,159,-74,-197,-57,-199,-30,-129,292,-142,-194,-31,-92,478,-225,-371,0,158,113,-294,-391,-207,146,-210,-404,-458,68,-33,-25,-25,355,53,8,129,54,69,84,-21,151,-72,161,-108,62,-103,18,-82,119,-88,-426,70,-355,-260,-315,70,-421,11,-218,-10,139,331,231,116,-233,74,165,-173,-85,12,-285,71,162,-39,116,-232,197,-71,89,-47,135,-340,82,63,79,203,-181,129,-318,-240,108,-76,-40,118,-276,-280,-209,]], 1321809)
    ]:
        nums = case[0]
        print 'Original {}, set {}'.format(len(nums), len(set(nums)))
        res = reverse_pairs(nums)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test_tree()
    test_counting()
    for i in range(100):
        test()

    print 'All tests passed'