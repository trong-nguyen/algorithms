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

class Node(object):
    """docstring for Node"""
    def __init__(self, weight=float('-inf')):
        super(Node, self).__init__()
        self.weight = weight
        self.children = {}

class Tree(object):
    """docstring for Tree"""
    def __init__(self, words):
        super(Tree, self).__init__()
        self.root = Node()
        self.build(words)

    def build(self, words, inversed_word=False):
        for weight, word in enumerate(words):
            w = word if not inversed_word else word[::-1]
            self.add_word(self.root, word, weight)


    @staticmethod
    def add_word(parent, word, weight):
        parent.weight = weight

        if not word:
            return

        char = word[0]
        if char not in parent.children:
            new_node = Node(weight)
            parent.children[char] = new_node

        Tree.add_word(new_node, word[1:], weight)

def search_word(word, root):
    if not word or word[0] not in root.children:
        return node.weight

    return search_word(word[1:], root.children[word[0]])



class WordFilter(object):

    def __init__(self, words):
        """
        :type words: List[str]
        """
        self.prefix_tree = Tree(words)
        self.suffix_tree = Tree(words, inversed_word=True)

    def f(self, prefix, suffix):
        """
        :type prefix: str
        :type suffix: str
        :rtype: int
        """
        prefix_weight = search_word(prefix, self.prefix_tree.root)
        suffix_weight = search_word(suffix, self.suffix_tree.root)

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
                print fail_string(res=res, ans=ans)
                sys.exit(0)



if __name__ == '__main__':
    test()
    test_long()
    test_leet()

