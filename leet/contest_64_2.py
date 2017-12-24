#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
You have a lock in front of you with 4 circular wheels. Each wheel has 10 slots: '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'. The wheels can rotate freely and wrap around: for example we can turn '9' to be '0', or '0' to be '9'. Each move consists of turning one wheel one slot.

The lock initially starts at '0000', a string representing the state of the 4 wheels.

You are given a list of deadends dead ends, meaning if the lock displays any of these codes, the wheels of the lock will stop turning and you will be unable to open it.

Given a target representing the value of the wheels that will unlock the lock, return the minimum total number of turns required to open the lock, or -1 if it is impossible.
Example 1:
Input: deadends = ["0201","0101","0102","1212","2002"], target = "0202"
Output: 6
Explanation:
A sequence of valid moves would be "0000" -> "1000" -> "1100" -> "1200" -> "1201" -> "1202" -> "0202".
Note that a sequence like "0000" -> "0001" -> "0002" -> "0102" -> "0202" would be invalid,
because the wheels of the lock become stuck after the display becomes the dead end "0102".
Example 2:
Input: deadends = ["8888"], target = "0009"
Output: 1
Explanation:
We can turn the last wheel in reverse to move from "0000" -> "0009".
Example 3:
Input: deadends = ["8887","8889","8878","8898","8788","8988","7888","9888"], target = "8888"
Output: -1
Explanation:
We can't reach the target without getting stuck.
Example 4:
Input: deadends = ["0000"], target = "8888"
Output: -1
Note:
The length of deadends will be in the range [1, 500].
target will not be in the list deadends.
Every string in deadends and the string target will be a string of 4 digits from the 10,000 possibilities '0000' to '9999'.


Solution:
    This is a shortest path graph problem
    We could apply breadth-first search with neighbors of a certain combination being the combination with one of
    its slot increased or reduced by 1

    ie: neighbors of 1352 are [[0]352, [2]352, 1[2]52, 1[4]52, 13[4]2, 13[6]2, 135[1], 135[3]]
"""

import sys
from utils.templates import fail_string


def turn(deadends, target):
    start = '0000'

    if start == target:
        return 0

    def neighbors(move):
        nb = []
        for i, m in enumerate(move):
            x = int(m)
            xn = (x+1) % 10
            xp = x-1 if x > 0 else 9
            for y in [xn, xp]:
                nb.append(move[:i] + str(y) + move[i+1:])
        return nb

    deadends = set(deadends)

    queue = {start}
    visited = {start}
    turns = 0
    while queue:
        next_queue = set()
        for node in queue:
            visited.add(node)
            for nb in neighbors(node):
                if nb not in visited and nb not in deadends:
                    next_queue.add(nb)

        # print queue, next_queue
        queue = next_queue

        turns += 1
        if target in queue:
            return turns

    return -1





def test():
    for case, ans in [
        ([["0201","0101","0102","1212","2002"], "0202"], 6),
        ([["8888"], "0009"], 1),
        ([["8887","8889","8878","8898","8788","8988","7888","9888"], "8888"], -1),
        ([["1002","1220","0122","0112","0121"], "1200"], 3),
    ]:
        res = turn(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()