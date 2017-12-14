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

SOLUTION:
    Sometimes brute-force appears to be quite a decent solution
    For each word and corresponding weight in the dictionary,
    take all possibilities of prefix - suffix of that word
    store it in a hashmap as a tuple of (pre-suffix) and value as weight
    lookup is armotized O(1)
    build time is O(nk^2) where n is the number of words in the dictionary
    and k is the maximum length of each word
"""

DEBUG = True

class PairTrie(object):
    """docstring for PairTrie"""
    def __init__(self, words):
        super(PairTrie, self).__init__()
        self.lookup = {}
        self.build(words)

    def build(self, words):
        for weight, word in enumerate(words):
            self.add_word(word, weight)

    def __str__(self):
        output = ''
        for (p, s), w in self.lookup.iteritems():
            output += '{} {}: {}\n'.format(p, s, w)
        return output


    def add_word(self, word, weight):
        if not word:
            # the only possibility is empty prefix and suffix
            # which is the empty query
            dual = ('', '')
            self.lookup[dual] = max(self.lookup.get(dual, weight), weight)

        # if not empty, there are k squared combinations of prefixes and suffixes
        # including the empty prefix and / or suffix
        # just loop over all possibilities and update weights to the higher values
        chars = [''] + list(word) + ['']
        n = len(chars)
        for i in range(n-1):
            prefix = ''.join(chars[:i+1])
            for j in range(n-1):
                suffix = ''.join(chars[j+1:])
                dual = (prefix, suffix)
                self.lookup[dual] = max(self.lookup.get(dual, weight), weight)

    def search(self, prefix, suffix):
        return self.lookup.get((prefix, suffix), None)

class WordFilter(object):

    def __init__(self, words):
        """
        :type words: List[str]
        """
        self.pair_trie = PairTrie(words)

    def f(self, prefix, suffix):
        """
        :type prefix: str
        :type suffix: str
        :rtype: int
        """
        res = self.pair_trie.search(prefix, suffix)
        return res if res != None else -1

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

