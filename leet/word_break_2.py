#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given a non-empty string s and a dictionary wordDict containing a list of non-empty words, add spaces in s to construct a sentence where each word is a valid dictionary word. You may assume the dictionary does not contain duplicate words.

Return all such possible sentences.

For example, given
s = "catsanddog",
dict = ["cat", "cats", "and", "sand", "dog"].

A solution is ["cats and dog", "cat sand dog"].

SOLUTION:
    Typical dynamical programming problem. Basically we rely on the fact that:
        - String completely comprised of and only of words found in the dictionary
    To:
        - Scan through the entire string, character by character, keep track of the current index
        - If a word in the dictionary is encountered, get the possible words on the remaining of the string

        M[i] = words found by looking ahead at the string from indices i
"""

def word_break(s, lookup_list):
    def scan(s, start, lookup, mem):
        # looking from start
        # print s[start:], mem
        if start >= len(s):
            return None

        if start in mem:
            # print 'Found in mem', start
            return mem[start]

        sentences = []
        word = ''
        for j in range(start, len(s)):
            word += s[j]
            # print word
            if word in lookup:
                if j == len(s) - 1:
                    sentences += [word]
                else:
                    ahead = scan(s, j+1, lookup, mem)
                    if not ahead:
                        continue

                    res = ['{} {}'.format(word, w) for w in ahead]
                    sentences += res
        mem[start] = sentences
        # print mem
        return sentences

    mem = {}
    return scan(s, 0, set(lookup_list), mem)

class Solution(object):
    def wordBreak(self, s, wordDict):
        """
        :type s: str
        :type wordDict: List[str]
        :rtype: List[str]
        """
        return word_break(s, wordDict)

import sys
from utils.templates import fail_string

def test():
    solution = Solution()
    for case, ans in [
        (['wordsandmeanings', ['words', 'and', 'meanings', 'wo', 'rds', 'mean', 'ings'] ], ['wo rds and mean ings', 'wo rds and meanings', 'words and mean ings', 'words and meanings']),
        (["catsanddog", ["cat", "cats", "and", "sand", "dog"]], ["cats and dog", "cat sand dog"]),
        (["catsanddog", ["catsand", "cats", "d", "d", "og"]], ["catsand d og"]),
        (["aaaabbbbccfw", ["a", "b", "c", "w", "f"]], ["a a a a b b b b c c f w"]),
    ]:
        res = solution.wordBreak(*case)
        try:
            assert sorted(res) == sorted(ans)
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()