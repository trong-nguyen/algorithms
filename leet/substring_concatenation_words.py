#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
You are given a string, s, and a list of words, words, that are all of the same length. Find all starting indices of substring(s) in s that is a concatenation of each word in words exactly once and without any intervening characters.

For example, given:
s: "barfoothefoobarman"
words: ["foo", "bar"]

You should return the indices: [0,9].
(order does not matter).

SOLUTION:
    Make use of the constant word length we can divide the string to a long list of words
    If k is the length of each word, there are n/k words in the string for each i=0..k offset
    For each offset:
        - We sweep over the long string, finding pattern
        - Pattern is the concatenated of the given list of words
        - Since the order of concatenation is not important, a pattern is considered matched
        once the occurences of each listed words reached the frequency given
        - We can keep the pattern in a map for each unique word with value being the occurences
        - While looping through the long words, if a word is found in the pattern / map, we
        reduce the counter by 0. If all counters for all words down to zero we have a match
        - If the counter for a single word becomes negative we reset the counter and count from
        the current position backword until the word that caused overmatching
        - If a word not found in the pattern we reset the counters
"""

import sys
from utils.templates import fail_string

def subcon(string, words):
    """
    Substring concatenation
    """

    n = len(string)
    m = len(words)
    if not words or not words[0]:
        # if no k then every indices can be used
        return list(range(n))

    k = len(words[0])
    if m == 1 and k == 1:
        the_word = words[0]
        return filter(lambda i: string[i] == the_word, range(n))

    # dict that counts word occurences and lookup
    occurences = {}
    for word in words:
        occurences[word] = occurences.get(word, 0) + 1

    results = []
    # Moving over n / k words with an offset from 0 to k
    # looking for match, backtrack if overmatched, log results if matched
    # the counters is to keep track of the matching words
    # the counter is in name-value with name the word and value the occurences
    # onces all occurences of the word down to zero we have a match
    # if one of the occurences shoot past zero (overmatching) we roll back the counters
    # of all the word come before it
    for offset in range(k):
        counters = dict(occurences)
        to_match = m
        for i in range(offset, n, k):
            if n - i < to_match * k:
                break
            w = string[i:i+k]
            if w in occurences:
                counters[w] -= 1
                # match
                if to_match == 1 and counters[w] == 0:
                    j = i - (m - 1) * k
                    w0 = string[j:j+k]
                    counters[w0] += 1
                    results.append(j)
                # overmatch
                elif counters[w] == -1:
                    # overmatch
                    counters = dict(occurences)
                    j = i
                    to_match = m
                    while j > i - (m - 1) * k:
                        wj = string[j:j+k]
                        if counters[wj] == 0:
                            break
                        to_match -= 1
                        counters[wj] -= 1
                        j -= k
                # else the counters is being filled, keep going
                else:
                    to_match -= 1
            # if non listed word is found, we reset the counters
            else:
                if to_match < m:
                    counters = dict(occurences) # reset
                to_match = m
    return results

def test():
    for case, ans in [
        (["aaabbbc", ["a","a","b","b","c"]], []),
        (["ababaab", ["ab","ba","ba"]], [1]),
        (["wordgoodgoodgoodbestword", ["word","good","best","good"]], [8]),
        (["barfoofoobarthefoobarman", ["bar","foo","the"]], [6,9,12]),
        (["xaksljfdhxxuux", []], range(len('xaksljfdhxxuux'))),
        (["xaksljfdhxxuux", ["x"]], [0, 9, 10, 13]),
        (["xaksljfdhxxuux", ["y"]], []),
        (["abcdef", ["abcdef"]], [0]),
        (["abcdef", ["abc", "def"]], [0]),
        (["abcdef", ["def", "abc"]], [0]),
        (["abcdef", ["def", "bca"]], []),
        (["aabbaabb", ["a", "a"]], [0, 4]),
        (["a"*10, ["a"]], list(range(10))),
        (["ababab", ["a", "b"]], [0, 1, 2, 3, 4]),
        (["barfoothefoobarman", ["foo", "bar"]], [0,9]),
        (["fobafo", ["fo", "ba"]], [0, 2]),
        (["abcdef"*100, list("abcdef")], range(99*len('abcdef') + 1)),
        (["abcdef"*100000, ["abcdef"]], range(0, 100000*len('abcdef'), len('abcdef'))),
    ]:
        res = subcon(*case)
        try:
            assert sorted(res) == sorted(ans)
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()