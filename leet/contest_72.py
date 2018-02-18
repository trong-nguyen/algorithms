#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""
class Solution_2(object):
    def isBipartite(self, graph):
        """
        Bipartite checking

        To be a valid bipartite graph, there exist a cut into {A/B}
        that all edges must have one node in A and another in B
        - Assume set A contains all nodes
        - Go into set A and for each edge moving one end to set B (either one is ok)
        - Check if set B contains any internal edges


        :type graph: List[List[int]]
        :rtype: bool
        """

        group_a = set(range(len(graph)))
        group_b = set()

        for i in group_a:
            if i in group_b:
                continue

            group_b.update(graph[i]) # add all connected nodes to i

        for i in group_b:
            if any([j in group_b for j in graph[i]]):
                return False

        return True


import math
import sys
from utils.templates import fail_string

class Solution(object):
    def letterCasePermutation(self, S):
        """
        :type S: str
        :rtype: List[str]
        """
        if not S:
            return ['']

        c = S[0]
        subs = self.letterCasePermutation(S[1:])

        if c.isdigit():
            return [c + s for s in subs]

        return [c.lower() + s for s in subs] + [c.upper() + s for s in subs]

def unit_test():
    pass

def test():
    solution = Solution()
    s = "a1b2"
    print solution.letterCasePermutation(s)

    s = "3z4"
    print solution.letterCasePermutation(s)

    s = "12345"
    print solution.letterCasePermutation(s)

    s = ""
    print solution.letterCasePermutation(s)

def test_2():
    solution = Solution_2()
    graph = [[1,3], [0,2], [1,3], [0,2]]
    assert solution.isBipartite(graph) == True

    graph = [[1,2,3], [0,2], [0,1,3], [0,2]]
    assert solution.isBipartite(graph) == False

if __name__ == '__main__':
    test_2()
    unit_test()
    test()