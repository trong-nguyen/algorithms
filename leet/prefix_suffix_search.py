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

class WordFilter(object):

    def __init__(self, words):
        """
        :type words: List[str]
        """
        DELIM = '@'
        weights = {}
        flatten_word = ''
        max_weight = len(words)
        for i, word in enumerate(words[::-1]):
            weights[len(flatten_word)] = max_weight - 1 - i
            flatten_word += DELIM + word

        self.flatten_word = flatten_word + DELIM
        self.weights = weights
        self.DELIM = DELIM

    def f(self, prefix, suffix):
        """
        :type prefix: str
        :type suffix: str
        :rtype: int
        """



        MAX_LENGTH = 10
        np = len(prefix)
        ns = len(suffix)

        NOT_FOUND = -1

        # overlap
        if np + ns > MAX_LENGTH and prefix[MAX_LENGTH-ns:] != suffix[:np+ns-MAX_LENGTH]:
            # if DEBUG:
            #     print '\n'
            #     print prefix, suffix
            #     print prefix[MAX_LENGTH-ns:], suffix[:np]
            #     print np, ns
            #     print 'Mismatched overlap'
            return NOT_FOUND

        components = [self.DELIM, prefix, suffix]
        if not prefix:
            pattern = re.compile(r'{0}[a-z]*{2}{0}'.format(*components))
        elif not suffix:
            pattern = re.compile(r'{0}{1}[a-z]*{0}'.format(*components))
        else:
            pattern = re.compile(r'(?={0}{1}[a-z]*{0}){0}[a-z]*{2}{0}'.format(*components))

        match = pattern.search(self.flatten_word)

        def print_debug():
            print self.flatten_word
            print '\tp:', prefix
            print '\ts:', suffix
            print '\tpattern:', pattern.pattern

        if not match:
            # if DEBUG:
            #     print '\n'
            #     print_debug()
            #     print 'word not found'
            return NOT_FOUND
        else:
            idx = match.start()
            # if DEBUG:
            #     print '\n'
            #     print match.group()
            #     print idx, self.weights[idx]
            #     print_debug()
            #     print 'word found'
            return self.weights[idx]



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

