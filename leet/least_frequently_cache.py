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

        self.tail.front = self.head
        self.head.rear = self.tail

    def insert_head(self, node):
        head, tail = self.head, self.tail

        rear = head.rear
        head.rear, node.front = node, head
        rear.front, node.rear = node, rear

    def insert_tail(self, node):
        tail = self.tail

        front = tail.front
        tail.front, node.rear = node, tail
        front.rear, node.front = node, front

    def remove_head(self):
        if self.empty():
            return

        pluck_off(self.head.rear)

    def remove_tail(self):
        if self.empty():
            return

        pluck_off(self.tail.front)

    def empty(self):
        return tail.front is head.rear



class Node(object):
    """docstring for Node"""
    def __init__(self, data=None):
        super(Node, self).__init__()
        self.data = data

def pluck_off(node):
    node.front.rear, node.rear.front = node.rear, node.front


class LFUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self.items = dict()
        self.linked_branches = LinkedList()
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

        return node.data['value']


    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: void
        """
        if key in self.items:
            node = self.items[key]
            increase_frequency(node)

        else:
            if len(self.items) == self.capacity:
                evict_one()

            self.insert_one(key, value)

    def create_branch(self, f):
        if f not in self.branches:
            self.branches[f] = Node(data={
                'key': f,
                'value': LinkedList()
                })
        return self.branches[f].data['value']

    def increase_frequency(self, node):
        """
        basically move a node from one branch to another with +1 higher frequency
        """
        f = node.data['frequency']

        branch = self.create_branch(f + 1)
        pluck_off(node)
        branch.data['value'].insert_head(node)
        node.data['frequency'] += 1

    def evict_one(self):
        branch = linked_branches.tail.front

        if not branch.data:
            return

        branch = branch.data['value']
        if branch.empty():
            return

        node = branch.tail.front
        pluck_off(node)

        if branch.empty():
            b = linked_branches[node.data['frequency']]
            pluck_off(b)
            del self.branches[b]

        del self.items[node.data['key']]

    def insert_one(self, key, value):
        branch = self.create_branch(1)

        node = Node({'key': key, 'value': value, 'frequency': 1})
        branch.insert_head(node)


import sys
from utils.templates import fail_string

def test():
    cache = LFUCache(2)

    # try:
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1, cache.get(1)       # returns 1
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