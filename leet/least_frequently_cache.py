#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Design and implement a data structure for Least Frequently Used (LFU) cache. It should support the following operations: get and put.

get(key) - Get the value (will always be positive) of the key if the key exists in the cache, otherwise return -1.
put(key, value) - Set or insert the value if the key is not already present. When the cache reaches its capacity, it should invalidate the least frequently used item before inserting a new item. For the purpose of this problem, when there is a tie (i.e., two or more keys that have the same frequency), the least recently used key would be evicted.

Follow up:
Could you do both operations in O(1) time complexity?

Example:

LFUCache cache = new LFUCache( 2 /* capacity */ );

cache.put(1, 1);
cache.put(2, 2);
cache.get(1);       // returns 1
cache.put(3, 3);    // evicts key 2
cache.get(2);       // returns -1 (not found)
cache.get(3);       // returns 3.
cache.put(4, 4);    // evicts key 1.
cache.get(1);       // returns -1 (not found)
cache.get(3);       // returns 3
cache.get(4);       // returns 4
"""
class LinkedList(object):
    """docstring for LinkedList"""
    def __init__(self):
        super(LinkedList, self).__init__()

        self.tail = Node()
        self.head = Node()

        self.tail.next = self.head
        self.head.previous = self.tail

class Node(object):
    """docstring for Node"""
    def __init__(self, data):
        super(Node, self).__init__()
        self.data = data

def pluck_off(node):
    node.next.previous, node.previous.next = node.previous, node.next


class Branch(object):
    def __init__(self):
        return

    def insert(self, node):


class LFUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self.items = dict()
        self.branches = dict()


    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key not in self.items:
            return -1

        node = self.items[key]

        self.increase_frequency(node)

        return node.value


    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: void
        """
        if key in self.items:
            node = self.items[keys]
            increase_frequency(node)

        else:
            if len(self.items) == self.capacity:
                evict_one()

            insert_one(key, value)

    def create_branch(self, f):
        if f not in self.branches:
            self.branches[f] = Branch(f)
        return self.branches[f]

    def increase_frequency(self, node):
        f = node.frequency

        branch = self.create_branch(f + 1)
        pluck_off(node)
        insert_to(branch)

    def evict_one(self):
        branch = tail.next
        pluck_off(branch.head.next)

    def insert_one(self, key, value):
        branch = self.create_branch(1)

        branch.add_node(key)

        if 1 not in self.branches:
            self.branches[1] =
        return


import sys
from utils.templates import fail_string

def test():
    cache = LFUCache(2)

    # try:
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1       # returns 1
    cache.put(3, 3)    # evicts key 2
    assert cache.get(2) == -1       # returns -1 (not found)
    assert cache.get(3) == 3       # returns 3.
    cache.put(4, 4)    # evicts key 1.
    assert cache.get(1) == -1       # returns -1 (not found)
    assert cache.get(3) == 3       # returns 3
    assert cache.get(4) == 4       # returns 4
    # except AssertionError as e:
    #     status = fail_string(res=None, ans=e, case=None)
    #     sys.exit(status)

if __name__ == '__main__':
    test()