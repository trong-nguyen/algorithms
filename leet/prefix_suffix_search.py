"""
Given many words, words[i] has weight i.

Design a class WordFilter that supports one function, WordFilter.f(String prefix, String suffix). It will return the word with given prefix and suffix with maximum weight. If no word exists, return -1.

Examples:
Input:
WordFilter(["apple"])
WordFilter.f("a", "e") // returns 0
WordFilter.f("b", "") // returns -1
Note:
words has length in range [1, 15000].
For each test case, up to words.length queries WordFilter.f may be made.
words[i] has length in range [1, 10].
prefix, suffix have lengths in range [0, 10].
words[i] and prefix, suffix queries consist of lowercase letters only.
"""

import re

DEBUG = True
TERMITE = '$'

class Node(object):
    """docstring for Node"""
    def __init__(self, weight=float('-inf')):
        super(Node, self).__init__()
        self.weight = weight
        self.children = {}
        self.reachables = {}

class Tree(object):
    """docstring for Tree"""
    def __init__(self, words):
        super(Tree, self).__init__()
        self.root = Node()
        self.build(words)

    def build(self, words):
        for weight, word in enumerate(words):
            self.add_word(self.root, word, weight)

    def __str__(self):
        output = ''
        heap = [self.root]
        labels = ['^']
        while heap:
            node = heap.pop(0)
            node_label = labels.pop(0)
            output += '{}: {}, next: {}, final: {}\n'.format(
                    node_label,
                    node.weight,
                    node.children.keys(),
                    node.reachables.keys()
                )
            heap += node.children.values()
            labels += node.children.keys()
        return output

    @staticmethod
    def add_word(parent, word, weight):
        parent.weight = weight

        # all reachable nodes from parent plus the tail
        for c in word + TERMITE:
            parent.reachables[c] = max(parent.reachables.get(c, weight), weight)

        if not word:
            node = parent.children.get(TERMITE, Node())
            node.weight = max(node.weight, weight)
            parent.children[TERMITE] = node
            return


        char = word[0]
        if char not in parent.children:
            parent.children[char] = Node(weight)

        node = parent.children[char]

        Tree.add_word(node, word[1:], weight)

def search_prefix_node(word, parent):
    # return the most specific node to the path defined by word
    # i.e. if the word is abc it return the node c situated at root->a->b->c
    if not word:
        return parent
    elif word[0] not in parent.children:
        return None

    return search_prefix_node(word[1:], parent.children[word[0]])

def search_prefix_suffix(prefix, suffix, root_node):
    NOT_FOUND = -1
    prefix_node = search_prefix_node(prefix, root_node)
    if not prefix_node:
        return NOT_FOUND

    if not suffix:
        return prefix_node.reachables[TERMITE]

    # linkable cases
    suffix_char = suffix[0]
    max_weight = prefix_node.reachables.get(suffix_char, NOT_FOUND)

    # stackable cases
    for i, c in enumerate(suffix):
        if stackable(prefix, suffix, i):
            suffix_path = suffix[i+1:]
            # if it matches from 0 to i
            # find if there is a path from i+1 to end of suffix
            node = search_prefix_node(suffix_path, prefix_node)
            if node and TERMITE in node.children:
                max_weight = max(max_weight, node.children[TERMITE].weight)


    # if DEBUG:
    #     print 'stackable'
    return max_weight

def stackable(prefix, suffix, i):
    # check if prefix matches part of suffix (1 or more)
    # i.e. prefix=abcd matches suffix=cd at i=1
    return prefix.endswith(suffix[:i+1])

class WordFilter(object):

    def __init__(self, words):
        """
        :type words: List[str]
        """
        self.prefix_tree = Tree(words)

        print self.prefix_tree

    def f(self, prefix, suffix):
        """
        :type prefix: str
        :type suffix: str
        :rtype: int
        """
        return search_prefix_suffix(prefix, suffix, self.prefix_tree.root)

# [[["abbbababbb","baaabbabbb","abababbaaa","abbbbbbbba","bbbaabbbaa","ababbaabaa","baaaaabbbb","babbabbabb","ababaababb","bbabbababa"]],["","abaa"],["babbab",""],["ab","baaa"],["baaabba","b"],["abab","abbaabaa"],["","aa"],["","bba"],["","baaaaabbbb"],["ba","aabbbb"],["baaa","aabbabbb"]]

from utils import fail_string

def test():
    words = ['apple']
    obj = WordFilter(words)
    for case, ans in [
        (('a', 'e'), 0),
        (('b', ''), -1),
    ]:
        res = obj.f(*case)
        assert res == ans, fail_string(res=res, ans=ans)


def test_long():
    words = ['apple', 'ape', 'ae', '']
    obj = WordFilter(words)
    for case, ans in [
        (('a', 'e'), 2),
        (('', ''), 3),
    ]:
        res = obj.f(*case)
        assert res == ans, fail_string(res=res, ans=ans)

import sys
def test_leet():
    null = 'null'
    for input2, output in [
        [
            [[["pop"]],["",""],["","p"],["","op"],["","pop"],["p",""],["p","p"],["p","op"],["p","pop"],["po",""],["po","p"],["po","op"],["po","pop"],["pop",""],["pop","p"],["pop","op"],["pop","pop"],["",""],["","p"],["","gp"],["","pgp"],["p",""],["p","p"],["p","gp"],["p","pgp"],["pg",""],["pg","p"],["pg","gp"],["pg","pgp"],["pgp",""],["pgp","p"],["pgp","gp"],["pgp","pgp"]],
            [null,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        ],
        [
            [[["abbbababbb","baaabbabbb","abababbaaa","abbbbbbbba","bbbaabbbaa","ababbaabaa","baaaaabbbb","babbabbabb","ababaababb","bbabbababa"]],["","abaa"],["babbab",""],["ab","baaa"],["baaabba","b"],["abab","abbaabaa"],["","aa"],["","bba"],["","baaaaabbbb"],["ba","aabbbb"],["baaa","aabbabbb"]],
            [null,5,7,2,1,5,5,3,6,6,1]
        ]
    ]:

        obj = WordFilter(input2[0][0])
        prefix_suffix = input2[1:]
        ans_array = output[1:]

        for case, ans in zip(prefix_suffix, ans_array):
            res = obj.f(*case)
            try:
                assert res == ans
            except AssertionError as e:
                print case
                print fail_string(res=res, ans=ans)
                sys.exit(0)



if __name__ == '__main__':
    test()
    test_long()
    test_leet()

